"""
Deterministic rule inspection engine for Inkloom Sentinel.
Executes high-speed regex pattern matching and exact phrase detection
without requiring LLM overhead for explicit policy breaches.
"""

import re
from typing import List, Dict, Any
from ..models import SeverityLevel

def run_deterministic_checks(text: str, rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scans text against active brand rules using compiled regexes and keyword catalogs.
    Returns structured violation candidates with character spans.
    """
    violations = []
    seen_spans = set()

    for rule in rules:
        if not rule.get("is_active", True):
            continue

        rule_code = rule["rule_code"]
        category = rule["category"]
        severity = SeverityLevel(rule["severity"])
        penalty = rule.get("penalty_points", 10)
        source = rule.get("approved_source", "Brand Governance Guidelines")
        approved_facts = rule.get("approved_facts", "")
        safe_guidance = rule.get("safe_alternative_guidance", "")
        title = rule.get("title", "")

        # 1. Regex Pattern Matching
        regex_pattern = rule.get("regex_pattern")
        if regex_pattern:
            try:
                for match in re.finditer(regex_pattern, text, re.IGNORECASE):
                    start, end = match.span()
                    span_key = (start, end)
                    if span_key in seen_spans:
                        continue
                    seen_spans.add(span_key)

                    flagged = match.group(0)
                    
                    # Synthesize specific suggested rewrite
                    suggested = generate_deterministic_rewrite(flagged, rule_code, safe_guidance)

                    violations.append({
                        "id": f"det_{rule_code}_{start}",
                        "rule_id": rule["id"],
                        "rule_code": rule_code,
                        "category": category,
                        "severity": severity,
                        "flagged_text": flagged,
                        "start_char": start,
                        "end_char": end,
                        "rule_citation": f"{rule_code}: {title}",
                        "approved_source": source,
                        "explanation": f"Contains flagged phrasing '{flagged}' which violates policy: {rule['description']}",
                        "suggested_rewrite": suggested,
                        "penalty": penalty,
                        "detection_method": "Deterministic Regex Linter"
                    })
            except Exception as e:
                print(f"Regex execution error on {rule_code}: {e}")

        # 2. Keywords substring search (if not already matched)
        keywords = rule.get("keywords", [])
        text_lower = text.lower()
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if not kw_clean or len(kw_clean) < 3:
                continue

            idx = 0
            while True:
                idx = text_lower.find(kw_clean, idx)
                if idx == -1:
                    break

                end = idx + len(kw_clean)
                span_key = (idx, end)
                if span_key not in seen_spans:
                    seen_spans.add(span_key)
                    flagged = text[idx:end]
                    suggested = generate_deterministic_rewrite(flagged, rule_code, safe_guidance)
                    violations.append({
                        "id": f"det_kw_{rule_code}_{idx}",
                        "rule_id": rule["id"],
                        "rule_code": rule_code,
                        "category": category,
                        "severity": severity,
                        "flagged_text": flagged,
                        "start_char": idx,
                        "end_char": end,
                        "rule_citation": f"{rule_code}: {title}",
                        "approved_source": source,
                        "explanation": f"Direct match with prohibited term '{flagged}'. {rule['description']}",
                        "suggested_rewrite": suggested,
                        "penalty": penalty,
                        "detection_method": "Keyword Matcher"
                    })
                idx += len(kw_clean)

    return violations

def generate_deterministic_rewrite(flagged: str, rule_code: str, guidance: str) -> str:
    """Provides high-quality, intent-preserving replacements for known violations."""
    flagged_lower = flagged.lower().strip()
    
    if "99.999%" in flagged_lower or "99.99%" in flagged_lower or "zero downtime" in flagged_lower:
        return "verified 99.95% enterprise uptime (backed by audited Q3 SLAs)"
    
    if "cloudtitan" in flagged_lower:
        return "traditional legacy cloud architectures"
    
    if "#1 cloud" in flagged_lower or "number 1 cloud" in flagged_lower:
        return "enterprise-grade cloud platform"
    
    if "unrivaled" in flagged_lower or "world-beating" in flagged_lower or "bulletproof" in flagged_lower:
        return "rigorously tested and resilient"
        
    if "10x developer productivity" in flagged_lower or "10x productivity" in flagged_lower:
        return "up to 38% faster deployment velocity across tested enterprise workloads"
        
    if "super chill" in flagged_lower:
        return "frictionless and reliable"
        
    if "legit fire" in flagged_lower or "insanely crazy" in flagged_lower:
        return "exceptionally high-performance"
        
    if "novacloud" == flagged_lower or "nova-cloud" == flagged_lower:
        return "NovaCloud"
        
    if "fully autonomous ai" in flagged_lower:
        return "AI-assisted copilot with human-in-the-loop governance"

    # Default fallback
    return guidance if guidance else flagged
