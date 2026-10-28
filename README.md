# Inkloom Sentinel 🛡️
### Intelligent Pre-Publication Brand Governance & Compliance Platform

[![We Code Coders Hackathon 2026](https://img.shields.io/badge/Hackathon-We%20Code%20Coders%202026-6366f1.svg)](https://forms.gle/gyRiHtQT3AnC3MdV6)
[![Round 2 - The Build](https://img.shields.io/badge/Round%202-The%20Build%20(100%20Pts)-10b981.svg)]()
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python%203.11+-009688.svg)](https://fastapi.tiangolo.com)
[![React Vite](https://img.shields.io/badge/Frontend-React%2018%20%7C%20Vite-61dafb.svg)](https://vitejs.dev)
[![Architecture](https://img.shields.io/badge/Governance-Deterministic%20%2B%20Grounded%20RAG-indigo.svg)]()

> **Team:** Binary Brains  
> **Team Members:**  
> 1. **Piyush Patel** (Team Leader — Full-Stack & System Integration)  
> 2. **Aryan Ponkiya** (AI/ML Engineer & Governance Pipeline Lead)  
> **Challenge Track:** Intelligent Brand Governance (Inkloom AI)

---

## 🎯 Executive Overview & Round 2 Mandate

In Round 2 (**The Build**), Team Binary Brains turned the Round 1 proposal into a fully operational, end-to-end intelligent brand compliance copilot. 

Unlike generic grammar linters (which have zero concept of proprietary company SLAs or trademark policies) or brittle regex keyword filters, **Inkloom Sentinel** combines a **high-speed deterministic policy layer** with **grounded vector retrieval (RAG)** against enterprise brand truth sheets. It identifies exact violations, explains regulatory and marketing liabilities, calculates a dynamic **Brand Health Index (BHI)**, suggests intent-preserving alternatives, and supports a formal human-in-the-loop cryptographic sign-off workflow.

---

## 🚀 Key Features Operational in Round 2

| Feature | Description | Technical Implementation |
| :--- | :--- | :--- |
| **⚡ Judge Fast-Track Testing** | 1-Click test presets for hackathon judges to verify Deliberate SLA breaches, Tone Drift, and 100% Compliant copy without manual typing. | Instant scenario injector with auto-inspection pipeline. |
| **🛡️ Grounded Truth Sheet Engine** | Active repository of enterprise brand rules, verified SLA telemetry (99.95% cap), banned competitor disparagement, and mandatory AI disclosures. | SQLite persistent storage + Vector TF-IDF / Jaccard semantic retrieval. |
| **🔍 Pre-Publication Content Studio** | Creator workspace with live reading telemetry, word counter, and animated scanning beam feedback. | React 18 + Vite with custom obsidian glass design system. |
| **📊 Brand Health Index (BHI)** | Empirical 0–100 score with calibrated severity deductions (-20 Critical, -15 Warning, -5 Advisory) and category breakdowns. | Mathematical penalty scoring algorithm with floor at 0. |
| **✨ 1-Click Intent-Preserving Fixes** | Evaluates violations and provides safe alternatives preserving original marketing punch while removing legal liabilities. | Inline / All-at-once text replacement engine with side-by-side diff view. |
| **✍️ Human-in-the-Loop Governance** | Creator submits draft $\rightarrow$ Reviewer approves/revises $\rightarrow$ Cryptographic signature hash (`SIG-XXXXX`) generated. | Role-based status state machine (`DRAFT` $\rightarrow$ `PENDING` $\rightarrow$ `APPROVED`). |
| **📜 Tamper-Evident Audit Ledger** | Immutable chronological record of scans, flagged breaches, reviewer notes, and SHA-256 content hashes. | SQLite audit table with structured JSON metadata. |

---

## 🏗️ System Architecture

```
[ Creator Draft / Marketing Collateral ]
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│            Inkloom Sentinel Frontend Studio            │
│       (React 18 + Vite + Obsidian Glass UI Engine)     │
└─────────────────────────┬──────────────────────────────┘
                          │ REST / JSON (Port 8000)
                          ▼
┌────────────────────────────────────────────────────────┐
│               FastAPI API Orchestrator                 │
├──────────────────────────┬─────────────────────────────┤
│   Deterministic Layer    │   Grounded Semantic Layer   │
│   • Compiled Regexes     │   • Vector Knowledge Store  │
│   • Prohibited Keywords  │   • Truth Sheet Retrieval   │
│   • Trademark Casing     │   • Section Citations       │
└─────────────┬────────────┴──────────────┬──────────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                BHI Mathematical Engine                 │
│        (Base 100 - Severity Penalty Deductions)        │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│         Human Review & Cryptographic Sign-Off          │
│   (Creator Queue -> Reviewer Signature -> Audit Log)   │
└────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Start Guide (Run in 60 Seconds)

### Prerequisites
- Python 3.10+
- Node.js 18+

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/inkloom-sentinel.git
cd inkloom-sentinel
```

### Step 2: Start Backend (FastAPI)
The backend automatically serves both the REST API and the pre-built React frontend:
```bash
python -m pip install fastapi uvicorn pydantic
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000/`** in your browser to use the full application!

*(Optional) For frontend hot-reloading development:*
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing with Judge Fast-Track Presets

At the top of the interface, click any of the **Judge Fast-Track** buttons:

1. **Deliberate Multi-Violation (Round 1 Case Study):**
   - Injects: *"NovaCloud is the #1 cloud guaranteeing 99.999% uptime with zero downtime. Our infrastructure beats CloudTitan and crushes legacy tools with 10x developer productivity. It provides super chill deployment vibes and fully autonomous AI."*
   - Flags: **SLA-401** (99.999% SLA cap), **COMP-204** (Named competitor deprecation), **SUP-102** (#1 cloud superlative), **DEV-305** (Unqualified 10x claim), **DISC-501** (Missing AI disclosure), **TONE-108** (Slang).
   - BHI drops to **0/100 (Critical Violation)**.
2. **Click "1-Click Fix All":**
   - Watch the editor transform into verified compliant copy citing 99.95% SLA and 38% velocity telemetry.
   - BHI rebounds to **95/100**.
3. **Click "Submit for Review" $\rightarrow$ Navigate to "Compliance Sign-Off" $\rightarrow$ Click "Approve":**
   - Triggers celebratory confetti and mints an official cryptographic compliance hash (e.g., `SIG-9BA7B42F8C1E`).

---

## 🌟 Three Major Improvements for Round 3 (The Finish)

1. **Calibrated Multi-Tenant BHI & Ambiguity Heatmaps:**
   - Statistical clustering (DBSCAN) over historical violation vectors to highlight brand guidelines that suffer repeated organizational misunderstandings.
2. **Multi-Modal Computer Vision Asset Governance:**
   - Programmatic inspection of marketing images: automated palette extraction, WCAG AAA contrast ratio compliance, and unapproved logo distortion detection.
3. **Headless CI/CD Pre-Commit Webhooks & SDK:**
   - Developer-first CLI tool gating markdown documentation, release notes, and pull requests directly in GitHub Actions.

---

## 👥 Team & Submission Information

* **Event:** We Code Coders Hackathon 2026
* **Round:** Round 2 — The Build (100 Points)
* **Team Name:** **Binary Brains**
* **Team Members:**
  * **Piyush Patel** — Team Leader (Full-Stack & System Integration)
  * **Aryan Ponkiya** — Team Member (AI/ML Engineer & Governance Pipeline Lead)
