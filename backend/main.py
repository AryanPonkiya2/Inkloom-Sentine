"""
Inkloom Sentinel — Intelligent Pre-Publication Brand Governance & Compliance Platform
Backend API Gateway & Core Orchestrator (FastAPI).
Engineered for We Code Coders Hackathon 2026 (Round 2 — The Build).
Team Binary Brains: Piyush Patel & Aryan Ponkiya.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid
import datetime
from typing import List, Dict, Any, Optional

from .models import (
    BrandRule, InspectionRequest, InspectionResult,
    ReviewActionRequest, SubmissionRecord, AuditLogEntry,
    ReviewStatus
)
from .database import (
    get_all_rules, add_rule, get_audit_logs, log_audit_event,
    get_submissions, save_submission, update_submission_review,
    hash_content
)
from .engine.copilot import analyze_content_governance

app = FastAPI(
    title="Inkloom Sentinel API",
    description="Intelligent Pre-Publication Brand Governance & Compliance Platform",
    version="2.0.0"
)

# Enable CORS for local dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Curated Presets for Hackathon Judges
SAMPLE_PRESETS = [
    {
        "id": "preset_deliberate_critical",
        "title": "Deliberate Multi-Violation (Round 1 Case Study)",
        "channel": "Enterprise Landing Page & Tech Blog",
        "author": "Piyush Patel (Creator)",
        "badge": "High Risk Violations",
        "description": "Contains unsupported 99.999% SLA claim, competitor disparagement, and 10x multiplier hype.",
        "text": "NovaCloud is the #1 cloud guaranteeing 99.999% uptime with zero downtime. Our infrastructure beats CloudTitan and crushes legacy tools with 10x developer productivity. It provides super chill deployment vibes and fully autonomous AI."
    },
    {
        "id": "preset_tone_hype",
        "title": "Tone & Brand Voice Drift",
        "channel": "LinkedIn & Social Copy",
        "author": "Agency Partner",
        "badge": "Tone Inconsistencies",
        "description": "Informal internet slang, missing camelCase trademark formatting, and unverified superlatives.",
        "text": "Check out novacloud for unrivaled speed and legit fire performance! Our silver bullet platform makes microservices insanely crazy fast with bulletproof security."
    },
    {
        "id": "preset_fully_compliant",
        "title": "Verified 100% Compliant Release",
        "channel": "Global Press Release",
        "author": "Aryan Ponkiya (Reviewer)",
        "badge": "100% Brand Compliant",
        "description": "Grounded in verified enterprise truth sheets, citing 99.95% SLA and professional corporate tone.",
        "text": "NovaCloud delivers verified 99.95% enterprise uptime backed by Q3 SLA telemetry to help engineering teams deploy reliably. In verified benchmark testing across enterprise repositories, deployment velocity accelerated by up to 38%."
    }
]

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "platform": "Inkloom Sentinel",
        "version": "2.0.0",
        "round": "Round 2 — The Build",
        "team": "Binary Brains (Piyush Patel & Aryan Ponkiya)",
        "modules": {
            "deterministic_engine": "ACTIVE",
            "grounded_rag_retriever": "ACTIVE",
            "bhi_scoring_engine": "ACTIVE",
            "audit_trail": "ACTIVE",
            "human_governance_workflow": "ACTIVE"
        }
    }

@app.get("/api/presets")
def get_presets():
    """Returns instant test scenarios for hackathon judges."""
    return SAMPLE_PRESETS

@app.get("/api/rules")
def list_rules():
    """Returns active brand rules and truth sheets."""
    return get_all_rules()

@app.post("/api/rules")
def create_rule(rule: BrandRule):
    """Allows brand administrators to register or update brand rules."""
    rule_dict = rule.dict()
    add_rule(rule_dict)
    log_audit_event(
        action_type="RULE_REGISTERED",
        actor="Brand Administrator",
        resource_id=rule.id,
        summary=f"Registered rule {rule.rule_code}: {rule.title}",
        text=rule.description,
        metadata={"category": rule.category, "severity": rule.severity}
    )
    return {"message": "Rule successfully registered", "rule": rule_dict}

@app.post("/api/inspect")
def inspect_content(req: InspectionRequest):
    """
    Core inspection endpoint: runs deterministic regex and grounded RAG evaluation.
    Calculates Brand Health Index (BHI) and produces intent-preserving rewrites.
    """
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Content text cannot be empty.")

    rules = get_all_rules()
    analysis = analyze_content_governance(
        text=req.text,
        rules=rules,
        enable_deep=req.enable_deep_reasoning
    )

    result_id = f"insp_{uuid.uuid4().hex[:8]}"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Record scan in audit trail
    log_audit_event(
        action_type="PRE_PUBLICATION_SCAN",
        actor=req.author,
        resource_id=result_id,
        summary=f"Inspected draft '{req.title}' ({req.channel}). BHI Score: {analysis['brand_health_index']}/100 with {len(analysis['violations'])} violations flagged.",
        text=req.text,
        metadata={
            "bhi": analysis["brand_health_index"],
            "violations_count": len(analysis["violations"]),
            "risk_level": analysis["risk_level"]
        }
    )

    return {
        "id": result_id,
        "title": req.title,
        "channel": req.channel,
        "author": req.author,
        "timestamp": now_str,
        "original_text": req.text,
        "clean_text_preview": analysis["clean_text_preview"],
        "brand_health_index": analysis["brand_health_index"],
        "status": analysis["status"],
        "risk_level": analysis["risk_level"],
        "violations": analysis["violations"],
        "deterministic_count": analysis["deterministic_count"],
        "rag_count": analysis["rag_count"],
        "execution_time_ms": analysis["execution_time_ms"],
        "category_scores": analysis["category_scores"]
    }

@app.post("/api/submissions")
def create_submission(sub_data: Dict[str, Any]):
    """Creates a submission for Human Review & Governance Sign-Off."""
    sub_id = f"sub_{uuid.uuid4().hex[:8]}"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "id": sub_id,
        "title": sub_data.get("title", "Untitled Draft"),
        "author": sub_data.get("author", "Content Creator"),
        "channel": sub_data.get("channel", "Enterprise Channel"),
        "created_at": now_str,
        "updated_at": now_str,
        "status": ReviewStatus.PENDING_REVIEW.value,
        "bhi_score": sub_data.get("brand_health_index", 100),
        "violations_count": len(sub_data.get("violations", [])),
        "original_text": sub_data.get("original_text", ""),
        "current_text": sub_data.get("current_text", sub_data.get("original_text", "")),
        "reviewer_name": None,
        "reviewer_role": None,
        "reviewer_notes": None,
        "signature_hash": None
    }

    save_submission(record)

    log_audit_event(
        action_type="SUBMISSION_QUEUED",
        actor=record["author"],
        resource_id=sub_id,
        summary=f"Draft submitted for Human Review & Governance Sign-Off. Initial BHI: {record['bhi_score']}/100",
        text=record["current_text"]
    )

    return {"message": "Draft submitted for formal review", "submission": record}

@app.get("/api/submissions")
def list_submissions():
    """Lists all submissions in the review pipeline."""
    return get_submissions()

@app.post("/api/submissions/{sub_id}/review")
def review_submission(sub_id: str, action: ReviewActionRequest):
    """Executes human review approval/rejection and signs with cryptographic hash."""
    updated = update_submission_review(
        sub_id=sub_id,
        status=action.action.value,
        reviewer_name=action.reviewer_name,
        reviewer_role=action.reviewer_role,
        notes=action.feedback_notes,
        approved_text=action.approved_text
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Submission not found")

    return {"message": f"Submission marked as {action.action.value}", "submission": updated}

@app.get("/api/audit-logs")
def list_audit_logs(limit: int = 50):
    """Returns the immutable tamper-evident governance audit log."""
    return get_audit_logs(limit)

@app.get("/api/analytics")
def get_analytics():
    """Returns executive governance metrics and Brand Health trends."""
    submissions = get_submissions()
    rules = get_all_rules()
    logs = get_audit_logs(100)

    total_subs = len(submissions)
    approved_count = sum(1 for s in submissions if s.get("status") == "APPROVED")
    pending_count = sum(1 for s in submissions if s.get("status") == "PENDING_REVIEW")
    avg_bhi = round(sum(s.get("bhi_score", 0) for s in submissions) / total_subs, 1) if total_subs > 0 else 92.5

    return {
        "total_submissions": total_subs,
        "approved_count": approved_count,
        "pending_count": pending_count,
        "average_bhi": avg_bhi,
        "active_rules_count": len(rules),
        "total_audit_events": len(logs),
        "compliance_rate": f"{round((approved_count / total_subs * 100), 1) if total_subs else 100}%"
    }

# Mount static build files if frontend/dist exists
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {
            "message": "Inkloom Sentinel Backend API is running.",
            "docs": "/docs",
            "health": "/api/health",
            "note": "Frontend is available on Vite dev server (port 5173) or run build for unified serving."
        }
