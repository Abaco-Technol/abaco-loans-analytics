"""Unit tests for MYPEBusinessRules."""
from __future__ import annotations

import pytest

from streamlit_app.utils.business_rules import ApprovalDecision, IndustryType, MYPEBusinessRules, RiskLevel


def test_high_risk_classification_flags_multiple_reasons():
    metrics = {"dpd": 120, "utilization": 0.95, "npl_ratio": 0.07, "collection_rate": 0.7}
    is_high, reasons = MYPEBusinessRules.classify_high_risk(metrics)

    assert is_high is True
    assert "Utilization" in " ".join(reasons)
    assert len(reasons) >= 3


def test_industry_adjustment_rewards_high_contribution():
    adjustment = MYPEBusinessRules.calculate_industry_adjustment(IndustryType.MANUFACTURING)
    assert adjustment > 1.0


def test_classify_npl_threshold():
    is_npl, message = MYPEBusinessRules.classify_npl(120)
    assert is_npl is True
    assert "NPL" in message


def test_rotation_target_message():
    rotation, meets, message = MYPEBusinessRules.check_rotation_target(total_revenue=500000, avg_balance=100000)
    assert pytest.approx(rotation, rel=1e-3) == 5
    assert meets is True
    assert "meets" in message.lower()


def test_evaluate_facility_approval_recommends_collateral_for_high_risk():
    metrics = {
        "dpd": 45,
        "utilization": 0.88,
        "npl_ratio": 0.06,
        "collection_rate": 0.8,
        "revenue": 220000,
        "avg_balance": 90000,
        "industry": IndustryType.TRADE,
    }
    decision: ApprovalDecision = MYPEBusinessRules.evaluate_facility_approval(
        facility_amount=200000, customer_metrics=metrics, collateral_value=50000
    )

    assert decision.approved is False
    assert decision.risk_level == RiskLevel.HIGH
    assert decision.required_collateral > 0
    assert decision.recommended_amount <= 200000
    assert decision.reasons
