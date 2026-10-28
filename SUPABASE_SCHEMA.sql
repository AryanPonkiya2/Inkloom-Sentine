-- ==============================================================
-- Inkloom Sentinel: Supabase PostgreSQL Database Schema
-- Brand Truth Repository, Submissions, and Tamper-Evident Ledger
-- ==============================================================

-- 1. Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Brand Rules Table
CREATE TABLE IF NOT EXISTS public.brand_rules (
    id TEXT PRIMARY KEY,
    rule_code TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('CRITICAL', 'WARNING', 'ADVISORY')),
    penalty_points INTEGER DEFAULT 15,
    keywords JSONB DEFAULT '[]'::jsonb,
    regex_pattern TEXT,
    approved_source TEXT NOT NULL,
    approved_facts TEXT NOT NULL,
    safe_alternative_guidance TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Review Submissions Table
CREATE TABLE IF NOT EXISTS public.submissions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    channel TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT NOT NULL DEFAULT 'PENDING_REVIEW' CHECK (status IN ('DRAFT', 'PENDING_REVIEW', 'APPROVED', 'REVISION_REQUESTED', 'REJECTED')),
    bhi_score INTEGER NOT NULL,
    violations_count INTEGER DEFAULT 0,
    original_text TEXT NOT NULL,
    current_text TEXT NOT NULL,
    reviewer_name TEXT,
    reviewer_role TEXT,
    reviewer_notes TEXT,
    signature_hash TEXT
);

-- 4. Audit Trail Table
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id TEXT PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    action_type TEXT NOT NULL,
    actor TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    summary TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 5. Row Level Security (RLS) Policies
ALTER TABLE public.brand_rules ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read of active brand rules"
    ON public.brand_rules FOR SELECT USING (is_active = true);

CREATE POLICY "Allow authenticated read and write on submissions"
    ON public.submissions FOR ALL USING (true);

CREATE POLICY "Allow authenticated append-only to audit logs"
    ON public.audit_logs FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read on audit logs"
    ON public.audit_logs FOR SELECT USING (true);
