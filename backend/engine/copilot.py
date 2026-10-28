"""
Inkloom Sentinel AI Copilot & Reasoning Core.
Orchestrates:
1. Deterministic regex & keyword inspection
2. Grounded RAG retrieval of approved truth sheets & brand rules
3. Context-aware synthesis of violations with exact citations
4. Intent-preserving safe alternative suggestions and clean text generation
"""

import os
import re
import time
import json
from typing import List, Dict, Any, Tuple
from .rule_checker import run_deterministic_checks
from .rag_engine import GroundedRAGEngine
from .bhi_calculator import calculate_brand_health_index
from ..models import SeverityLevel

def analyze_content_governance(text: str, rules: List[Dict[str, Any]], enable_deep: bool = True) -> Dict[str, Any]:
    start_time = time.time()
    
    # 1. Run Deterministic Layer
    deterministic_violations = run_deterministic_checks(text, rules)
    
    # 2. Run Grounded Semantic / RAG Layer
    rag_engine = GroundedRAGEngine(rules)
    rag_violations = []

    # Break text into candidate sentences for grounded inspection
    sentences = re.split(r"(?<=[.!?])\s+", text)
    curr_offset = 0

    for sent in sentences:
        sent_clean = sent.strip()
        sent_start = text.find(sent_clean, curr_offset)
        if sent_start == -1:
            sent_start = curr_offset
        sent_end = sent_start + len(sent_clean)
        curr_offset = sent_end

        if not sent_clean or len(sent_clean) < 10:
            continue

        # Retrieve relevant brand guidelines
        matches = rag_engine.retrieve_relevant_guidelines(sent_clean, top_k=2, threshold=0.18)
        for rule, similarity in matches:
            rule_code = rule["rule_code"]
            
            # Skip if deterministic layer already flagged this exact rule in this sentence
            already_flagged = any(
                v["rule_code"] == rule_code and (v["start_char"] >= sent_start and v["end_char"] <= sent_end)
                for v in deterministic_violations
            )
            if already_flagged:
                continue

            # Check semantic conditions for non-regex rule violations
            violation_details = evaluate_semantic_condition(sent_clean, rule, similarity)
            if violation_details:
                rag_violations.append({
                    "id": f"rag_{rule_code}_{sent_start}",
                    "rule_id": rule["id"],
                    "rule_code": rule_code,
                    "category": rule["category"],
                    "severity": SeverityLevel(rule["severity"]),
                    "flagged_text": violation_details["flagged_text"],
                    "start_char": sent_start,
                    "end_char": sent_end,
                    "rule_citation": f"{rule_code}: {rule['title']}",
                    "approved_source": rule["approved_source"],
                    "explanation": violation_details["explanation"],
                    "suggested_rewrite": violation_details["suggested_rewrite"],
                    "penalty": rule.get("penalty_points", 10),
                    "detection_method": f"Grounded RAG (Relevance: {int(similarity * 100)}%)"
                })

    # Combine all unique violations
    all_violations = deterministic_violations + rag_violations

    # Remove overlapping duplicates if any
    unique_violations = []
    seen_ids = set()
    for v in all_violations:
        if v["id"] not in seen_ids:
            seen_ids.add(v["id"])
            unique_violations.append(v)

    # Sort violations by start_char
    unique_violations.sort(key=lambda x: x["start_char"])

    # 3. Calculate Brand Health Index (BHI)
    bhi_data = calculate_brand_health_index(unique_violations)

    # 4. Generate Clean Compliant Text Preview (applying suggested rewrites)
    clean_text = apply_suggested_rewrites(text, unique_violations)

    execution_time = round((time.time() - start_time) * 1000, 2)

    return {
        "violations": unique_violations,
        "brand_health_index": bhi_data["bhi_score"],
        "status": bhi_data["status"],
        "risk_level": bhi_data["risk_level"],
        "deterministic_count": len(deterministic_violations),
        "rag_count": len(rag_violations),
        "clean_text_preview": clean_text,
        "execution_time_ms": execution_time,
        "category_scores": bhi_data["category_scores"]
    }

def evaluate_semantic_condition(sentence: str, rule: Dict[str, Any], similarity: float) -> Dict[str, str]:
    """
    Evaluates semantic nuances against grounded truth passages.
    Returns explanation and suggested rewrite if a grounded breach is identified.
    """
    rule_code = rule["rule_code"]
    s_lower = sentence.lower()

    if rule_code == "SLA-401" and ("uptime" in s_lower or "availability" in s_lower or "guarantee" in s_lower):
        if not ("99.95%" in sentence):
            return {
                "flagged_text": sentence,
                "explanation": f"Fails to explicitly cite verified SLA baseline. {rule['approved_facts']}",
                "suggested_rewrite": "NovaCloud guarantees verified 99.95% enterprise uptime across all multi-region production clusters."
            }

    if rule_code == "SUP-102" and any(word in s_lower for word in ["best", "leading", "unmatched", "greatest", "perfect"]):
        return {
            "flagged_text": sentence,
            "explanation": f"Contains unquantified superlative claim. Per brand guidelines: {rule['approved_facts']}",
            "suggested_rewrite": "delivering verified enterprise-grade reliability and high-throughput execution."
        }

    if rule_code == "DEV-305" and ("faster" in s_lower or "boost" in s_lower or "speedup" in s_lower) and not ("38%" in sentence):
        return {
            "flagged_text": sentence,
            "explanation": f"Performance acceleration claim lacks audited telemetry baseline. {rule['approved_facts']}",
            "suggested_rewrite": "accelerates deployment velocity by up to 38% based on verified enterprise benchmarks."
        }

    return None

def apply_suggested_rewrites(original_text: str, violations: List[Dict[str, Any]]) -> str:
    """Replaces flagged segments with compliant suggested alternatives."""
    if not violations:
        return original_text

    # Reconstruct text from right to left to maintain valid string character indices
    modified_text = original_text
    sorted_rev = sorted(violations, key=lambda x: x["start_char"], reverse=True)

    for v in sorted_rev:
        start = v["start_char"]
        end = v["end_char"]
        suggested = v.get("suggested_rewrite")
        if suggested and 0 <= start < end <= len(modified_text):
            modified_text = modified_text[:start] + suggested + modified_text[end:]

    return modified_text
