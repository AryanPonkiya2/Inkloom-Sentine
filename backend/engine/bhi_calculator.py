"""
Brand Health Index (BHI) Engine for Inkloom Sentinel.
Implements the calibrated mathematical penalty scoring model described in Section 5.1
of the Round 1 proposal. Produces an aggregate 0-100 score and category breakdowns.
"""

from typing import List, Dict, Any

def calculate_brand_health_index(violations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates BHI starting from 100 points, subtracting calibrated penalties
    based on violation severity and regulatory liability.
    """
    base_score = 100
    total_deductions = 0

    category_stats = {
        "Factual Claims & SLAs": {"deductions": 0, "violations": 0},
        "Prohibited Nomenclature": {"deductions": 0, "violations": 0},
        "Voice & Tone Consistency": {"deductions": 0, "violations": 0},
        "Legal & Trademark Disclaimers": {"deductions": 0, "violations": 0},
        "Visual & Formatting Guidelines": {"deductions": 0, "violations": 0}
    }

    for v in violations:
        penalty = v.get("penalty", 10)
        total_deductions += penalty
        cat = v.get("category", "Voice & Tone Consistency")
        if cat in category_stats:
            category_stats[cat]["deductions"] += penalty
            category_stats[cat]["violations"] += 1
        else:
            category_stats["Voice & Tone Consistency"]["deductions"] += penalty
            category_stats["Voice & Tone Consistency"]["violations"] += 1

    final_score = max(0, min(100, base_score - total_deductions))

    # Risk level classification
    if final_score >= 90 and len(violations) == 0:
        status = "PASSED"
        risk_level = "Zero Risk — Brand Compliant"
    elif final_score >= 70:
        status = "MODERATE_RISK"
        risk_level = "Requires Review & Minor Corrections"
    else:
        status = "CRITICAL_VIOLATION"
        risk_level = "High Regulatory & Brand Liability"

    # Category breakdowns (max 100 per category)
    breakdowns = []
    for cat_name, stats in category_stats.items():
        cat_score = max(0, 100 - (stats["deductions"] * 2))
        breakdowns.append({
            "category": cat_name,
            "score": cat_score,
            "total_violations": stats["violations"]
        })

    return {
        "bhi_score": final_score,
        "status": status,
        "risk_level": risk_level,
        "total_deductions": total_deductions,
        "category_scores": breakdowns
    }
