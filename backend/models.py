"""
Data models and schemas for Inkloom Sentinel Brand Governance Platform.
Supports strict Pydantic validation across all API boundaries.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import datetime

class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    ADVISORY = "ADVISORY"

class RuleCategory(str, Enum):
    FACTUAL_SLA = "Factual Claims & SLAs"
    BANNED_VOCAB = "Prohibited Nomenclature"
    TONE_VOICE = "Voice & Tone Consistency"
    REGULATORY = "Legal & Trademark Disclaimers"
    VISUAL_STYLE = "Visual & Formatting Guidelines"

class ReviewStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    REJECTED = "REJECTED"

class BrandRule(BaseModel):
    id: str
    rule_code: str
    category: RuleCategory
    title: str
    description: str
    severity: SeverityLevel
    penalty_points: int = 15
    keywords: List[str] = []
    regex_pattern: Optional[str] = None
    approved_source: str
    approved_facts: str
    safe_alternative_guidance: str
    is_active: bool = True

class InspectionRequest(BaseModel):
    title: str = "Marketing Campaign Copy"
    channel: str = "Enterprise Landing Page"
    author: str = "Piyush Patel"
    text: str
    enable_deep_reasoning: bool = True

class Violation(BaseModel):
    id: str
    rule_id: str
    rule_code: str
    category: str
    severity: SeverityLevel
    flagged_text: str
    start_char: int
    end_char: int
    rule_citation: str
    approved_source: str
    explanation: str
    suggested_rewrite: str
    penalty: int
    detection_method: str = "Deterministic & Grounded RAG"

class CategoryBreakdown(BaseModel):
    category: str
    score: int
    total_violations: int

class InspectionResult(BaseModel):
    id: str
    title: str
    channel: str
    author: str
    timestamp: str
    original_text: str
    clean_text_preview: str
    brand_health_index: int
    status: str
    risk_level: str
    violations: List[Violation]
    deterministic_count: int
    rag_count: int
    execution_time_ms: float
    category_scores: List[CategoryBreakdown]

class ReviewActionRequest(BaseModel):
    submission_id: str
    action: ReviewStatus
    reviewer_name: str = "Aryan Ponkiya"
    reviewer_role: str = "Lead Brand Custodian"
    feedback_notes: str = ""
    approved_text: Optional[str] = None

class SubmissionRecord(BaseModel):
    id: str
    title: str
    author: str
    channel: str
    created_at: str
    updated_at: str
    status: ReviewStatus
    bhi_score: int
    violations_count: int
    original_text: str
    current_text: str
    reviewer_name: Optional[str] = None
    reviewer_role: Optional[str] = None
    reviewer_notes: Optional[str] = None
    signature_hash: Optional[str] = None

class AuditLogEntry(BaseModel):
    id: str
    timestamp: str
    action_type: str
    actor: str
    resource_id: str
    summary: str
    content_hash: str
    metadata: Dict[str, Any] = {}
