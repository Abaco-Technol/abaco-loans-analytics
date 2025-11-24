"""Business rules used in the Streamlit application."""

from __future__ import annotations

from enum import Enum


class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class MYPEBusinessRules:
    """Risk rules for micro and small enterprise lending."""

    @staticmethod
    def calculate_risk_level(pod: float, approved: bool) -> RiskLevel:
        """Assign risk buckets without overwriting higher levels erroneously."""

        if pod <= 0.15:
            risk_level = RiskLevel.LOW
        elif pod <= 0.30:
            risk_level = RiskLevel.MEDIUM
        elif pod <= 0.50:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL

        # Escalate risk for unapproved applicants while preserving the ladder.
        if not approved and risk_level == RiskLevel.LOW:
            return RiskLevel.MEDIUM

        return risk_level
