"""
Database operations and initial brand knowledge seeding for Inkloom Sentinel.
Uses SQLite for zero-configuration, reliable persistence with full audit trails.
"""

import sqlite3
import json
import os
import hashlib
import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "sentinel.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

DEFAULT_BRAND_RULES = [
    {
        "id": "rule_01",
        "rule_code": "SLA-401",
        "category": "Factual Claims & SLAs",
        "title": "Strict SLA & Uptime Guarantee Capping",
        "description": "Never state or promise uptime exceeding verified infrastructure SLA of 99.95%. Exaggerated availability claims create immediate regulatory and contractual liabilities.",
        "severity": "CRITICAL",
        "penalty_points": 20,
        "keywords": ["99.999%", "99.99%", "100% uptime", "zero downtime", "never goes down"],
        "regex_pattern": r"(99\.999%|99\.99%|100%\s*uptime|zero\s*downtime)",
        "approved_source": "Enterprise Master Services Agreement §4.1 (Q3 Verified SLA Benchmark)",
        "approved_facts": "NovaCloud infrastructure is verified and audited at 99.95% production uptime across all multi-region deployments.",
        "safe_alternative_guidance": "State verified 99.95% enterprise SLA benchmark backed by active multi-region redundancy.",
        "is_active": True
    },
    {
        "id": "rule_02",
        "rule_code": "COMP-204",
        "category": "Prohibited Nomenclature",
        "title": "Unsubstantiated Competitor Deprecation & Named Bashing",
        "description": "Direct disparagement or unverified benchmark comparisons against named competitors (e.g. CloudTitan, MegaStack) is prohibited without certified third-party audit clearance.",
        "severity": "CRITICAL",
        "penalty_points": 20,
        "keywords": ["CloudTitan is obsolete", "beats CloudTitan", "MegaStack is insecure", "destroy CloudTitan", "crush CloudTitan"],
        "regex_pattern": r"(CloudTitan\s*(?:is\s*obsolete|sucks|fails|inferior)|beats\s*CloudTitan|destroy\s*CloudTitan)",
        "approved_source": "Legal & Brand Compliance Standards §7.2 (Fair Competition & Comparative Advertising)",
        "approved_facts": "Comparative claims must cite publicly audited industry benchmarks; named vendor attacks expose the company to tortious interference claims.",
        "safe_alternative_guidance": "Highlight architectural benefits (e.g. 'reduces cold starts by 45% vs traditional legacy hypervisors') rather than naming competitors pejoratively.",
        "is_active": True
    },
    {
        "id": "rule_03",
        "rule_code": "SUP-102",
        "category": "Voice & Tone Consistency",
        "title": "Ban on Unverifiable Superlatives & Empty Hype",
        "description": "Words like '#1 cloud', 'unrivaled', 'world-beating', 'bulletproof', and 'silver bullet' violate brand voice standards. Replace with measurable performance metrics.",
        "severity": "WARNING",
        "penalty_points": 15,
        "keywords": ["#1 cloud", "number 1 cloud", "unrivaled", "bulletproof", "world-beating", "best in the galaxy", "silver bullet"],
        "regex_pattern": r"(#1\s*cloud|number\s*1\s*cloud|unrivaled|bulletproof|world-beating|silver\s*bullet)",
        "approved_source": "Brand Voice & Editorial Style Manual §2.3 (Clarity & Authenticity)",
        "approved_facts": "NovaCloud maintains an authoritative, engineer-first tone based on concrete telemetry, not marketing puffery.",
        "safe_alternative_guidance": "State measured performance outcomes (e.g. 'industry-tested cloud infrastructure delivering sub-10ms packet routing').",
        "is_active": True
    },
    {
        "id": "rule_04",
        "rule_code": "DEV-305",
        "category": "Factual Claims & SLAs",
        "title": "Unqualified Multiplier Productivity Claims",
        "description": "Marketing claims citing multipliers like '10x developer productivity' or 'instant 100x speedup' are legally misleading unless accompanied by specific case study conditions.",
        "severity": "WARNING",
        "penalty_points": 15,
        "keywords": ["10x developer productivity", "10x productivity", "100x speedup", "instant 10x"],
        "regex_pattern": r"(\b10x\s*developer\s*productivity|\b100x\s*speedup|\b10x\s*productivity)",
        "approved_source": "Product Marketing Truth Sheet §8.4 (Telemetry & Productivity Claims)",
        "approved_facts": "Internal cohort testing demonstrated up to 38% faster CI/CD deployment cycles across tested enterprise repositories.",
        "safe_alternative_guidance": "Cite verified telemetry: 'delivering up to 38% faster deployment velocity as observed in benchmark tests'.",
        "is_active": True
    },
    {
        "id": "rule_05",
        "rule_code": "DISC-501",
        "category": "Legal & Trademark Disclaimers",
        "title": "Mandatory AI Disclosure on Generative Features",
        "description": "Any public feature description mentioning generative content generation or autonomous decision-making must include the required human-in-the-loop oversight disclaimer.",
        "severity": "WARNING",
        "penalty_points": 10,
        "keywords": ["fully autonomous AI", "ai replaces all humans", "100% automated without human"],
        "regex_pattern": r"(fully\s*autonomous\s*AI|ai\s*replaces\s*all\s*humans|100%\s*automated\s*without\s*human)",
        "approved_source": "EU AI Act & Corporate Governance Charter §9.1",
        "approved_facts": "All AI-assisted governance features operate strictly as human-in-the-loop copilots with authoritative editorial oversight.",
        "safe_alternative_guidance": "Clarify that AI accelerates initial policy checks while ultimate publishing authority remains in human control.",
        "is_active": True
    },
    {
        "id": "rule_06",
        "rule_code": "TONE-108",
        "category": "Voice & Tone Consistency",
        "title": "Informal Slang in Enterprise Collateral",
        "description": "Avoid colloquial internet slang like 'super chill', 'insanely crazy', 'vibes', or 'legit fire' in B2B press releases and investor-facing communications.",
        "severity": "ADVISORY",
        "penalty_points": 5,
        "keywords": ["super chill", "legit fire", "insanely crazy", "vibes are immaculate"],
        "regex_pattern": r"(\bsuper\s*chill\b|\blegit\s*fire\b|\binsanely\s*crazy\b|\bvibes\b)",
        "approved_source": "Editorial Tone Matrix — Corporate & Enterprise Channels",
        "approved_facts": "Communications to CTOs and procurement directors must convey rigorous reliability and professional composure.",
        "safe_alternative_guidance": "Use professional, composed phrasing such as 'frictionless onboarding' or 'high-confidence execution'.",
        "is_active": True
    },
    {
        "id": "rule_07",
        "rule_code": "TM-602",
        "category": "Legal & Trademark Disclaimers",
        "title": "Trademark Capitalization & Logo Spacing",
        "description": "The brand name must always be capitalized as 'NovaCloud' (camelCase style), never 'novacloud', 'NOVA CLOUD', or 'Nova-cloud'.",
        "severity": "ADVISORY",
        "penalty_points": 5,
        "keywords": ["novacloud", "Nova-cloud", "NOVA CLOUD"],
        "regex_pattern": r"(\bnovacloud\b|\bNova-cloud\b|\bNOVA\s*CLOUD\b)",
        "approved_source": "Trademark Style Guide §1.1 (Brand Asset Identity)",
        "approved_facts": "The registered corporate trademark is 'NovaCloud'. Proper case preservation protects international trademark standing.",
        "safe_alternative_guidance": "Ensure consistent camelCase capitalization: 'NovaCloud'.",
        "is_active": True
    }
]

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Brand Rules Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS brand_rules (
        id TEXT PRIMARY KEY,
        rule_code TEXT UNIQUE,
        category TEXT,
        title TEXT,
        description TEXT,
        severity TEXT,
        penalty_points INTEGER,
        keywords TEXT,
        regex_pattern TEXT,
        approved_source TEXT,
        approved_facts TEXT,
        safe_alternative_guidance TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    # Submissions & Approvals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        channel TEXT,
        created_at TEXT,
        updated_at TEXT,
        status TEXT,
        bhi_score INTEGER,
        violations_count INTEGER,
        original_text TEXT,
        current_text TEXT,
        reviewer_name TEXT,
        reviewer_role TEXT,
        reviewer_notes TEXT,
        signature_hash TEXT
    )
    """)

    # Audit Trail Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        action_type TEXT,
        actor TEXT,
        resource_id TEXT,
        summary TEXT,
        content_hash TEXT,
        metadata TEXT
    )
    """)

    conn.commit()

    # Seed Default Rules if empty
    cursor.execute("SELECT COUNT(*) FROM brand_rules")
    if cursor.fetchone()[0] == 0:
        for r in DEFAULT_BRAND_RULES:
            cursor.execute("""
            INSERT INTO brand_rules (
                id, rule_code, category, title, description, severity,
                penalty_points, keywords, regex_pattern, approved_source,
                approved_facts, safe_alternative_guidance, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r["id"], r["rule_code"], r["category"], r["title"], r["description"],
                r["severity"], r["penalty_points"], json.dumps(r["keywords"]),
                r["regex_pattern"], r["approved_source"], r["approved_facts"],
                r["safe_alternative_guidance"], 1 if r["is_active"] else 0
            ))
        conn.commit()

    # Seed Sample Submissions if empty
    cursor.execute("SELECT COUNT(*) FROM submissions")
    if cursor.fetchone()[0] == 0:
        sample_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO submissions (
            id, title, author, channel, created_at, updated_at, status,
            bhi_score, violations_count, original_text, current_text,
            reviewer_name, reviewer_role, reviewer_notes, signature_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "sub_demo_01",
            "NovaCloud Q4 Global Launch Press Release",
            "Piyush Patel (Creator)",
            "Enterprise Press Release",
            sample_time,
            sample_time,
            "APPROVED",
            95,
            0,
            "NovaCloud delivers verified 99.95% enterprise uptime backed by Q3 SLA telemetry to help engineering teams deploy reliably.",
            "NovaCloud delivers verified 99.95% enterprise uptime backed by Q3 SLA telemetry to help engineering teams deploy reliably.",
            "Aryan Ponkiya",
            "Lead Brand Governance Officer",
            "Verified against Q3 production telemetry and Brand Style Guide. Approved for global release.",
            "SIG-98A7B42F0C1E"
        ))
        
        # Log the audit entry
        cursor.execute("""
        INSERT INTO audit_logs (
            id, timestamp, action_type, actor, resource_id, summary, content_hash, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "log_init_01",
            sample_time,
            "SYSTEM_SEED_INITIALIZATION",
            "System Bootstrapper",
            "sub_demo_01",
            "Initialized system with verified sample submission and 7 active brand governance rules.",
            "HASH-INIT-001",
            json.dumps({"version": "2.0.0", "track": "We Code Coders Round 2"})
        ))
        conn.commit()

    conn.close()

# Public helper functions
def get_all_rules() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brand_rules WHERE is_active = 1")
    rows = cursor.fetchall()
    rules = []
    for row in rows:
        r = dict(row)
        r["keywords"] = json.loads(r["keywords"]) if r["keywords"] else []
        r["is_active"] = bool(r["is_active"])
        rules.append(r)
    conn.close()
    return rules

def add_rule(rule_data: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO brand_rules (
        id, rule_code, category, title, description, severity,
        penalty_points, keywords, regex_pattern, approved_source,
        approved_facts, safe_alternative_guidance, is_active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rule_data["id"], rule_data["rule_code"], rule_data["category"], rule_data["title"],
        rule_data["description"], rule_data["severity"], rule_data["penalty_points"],
        json.dumps(rule_data.get("keywords", [])), rule_data.get("regex_pattern", ""),
        rule_data["approved_source"], rule_data["approved_facts"],
        rule_data["safe_alternative_guidance"], 1 if rule_data.get("is_active", True) else 0
    ))
    conn.commit()
    conn.close()

def log_audit_event(action_type: str, actor: str, resource_id: str, summary: str, text: str, metadata: Dict[str, Any] = None):
    conn = get_connection()
    cursor = conn.cursor()
    log_id = f"log_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{hash_content(resource_id)[:4]}"
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chash = hash_content(text)
    meta_json = json.dumps(metadata or {})
    cursor.execute("""
    INSERT INTO audit_logs (id, timestamp, action_type, actor, resource_id, summary, content_hash, metadata)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (log_id, ts, action_type, actor, resource_id, summary, chash, meta_json))
    conn.commit()
    conn.close()

def get_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    logs = [dict(r) for r in rows]
    conn.close()
    return logs

def save_submission(sub: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO submissions (
        id, title, author, channel, created_at, updated_at, status,
        bhi_score, violations_count, original_text, current_text,
        reviewer_name, reviewer_role, reviewer_notes, signature_hash
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sub["id"], sub["title"], sub["author"], sub["channel"],
        sub["created_at"], sub["updated_at"], sub["status"],
        sub["bhi_score"], sub["violations_count"], sub["original_text"],
        sub["current_text"], sub.get("reviewer_name"), sub.get("reviewer_role"),
        sub.get("reviewer_notes"), sub.get("signature_hash")
    ))
    conn.commit()
    conn.close()

def get_submissions() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    subs = [dict(r) for r in rows]
    conn.close()
    return subs

def update_submission_review(sub_id: str, status: str, reviewer_name: str, reviewer_role: str, notes: str, approved_text: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions WHERE id = ?", (sub_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    current = dict(row)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sig_hash = f"SIG-{hashlib.sha256((sub_id + status + reviewer_name + now_str).encode('utf-8')).hexdigest()[:12].upper()}" if status == "APPROVED" else None
    
    final_text = approved_text if approved_text is not None else current["current_text"]
    
    cursor.execute("""
    UPDATE submissions SET
        status = ?,
        updated_at = ?,
        reviewer_name = ?,
        reviewer_role = ?,
        reviewer_notes = ?,
        current_text = ?,
        signature_hash = ?
    WHERE id = ?
    """, (status, now_str, reviewer_name, reviewer_role, notes, final_text, sig_hash, sub_id))
    conn.commit()
    
    cursor.execute("SELECT * FROM submissions WHERE id = ?", (sub_id,))
    updated_row = dict(cursor.fetchone())
    conn.close()
    
    log_audit_event(
        action_type=f"SUBMISSION_{status}",
        actor=f"{reviewer_name} ({reviewer_role})",
        resource_id=sub_id,
        summary=f"Submission status changed to {status}. Notes: {notes or 'None'}",
        text=final_text,
        metadata={"signature_hash": sig_hash}
    )
    
    return updated_row

# Initialize DB on load
init_db()
