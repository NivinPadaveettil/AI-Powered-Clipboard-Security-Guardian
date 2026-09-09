from dataclasses import dataclass


@dataclass
class RiskResult:
    category: str
    confidence: float
    risk_score: int
    risk_level: str
    explanation: str
    action: str
    timeout: int


RISK_TABLE = {

    "safe": RiskResult(
        "safe", 0, 0,
        "Low",
        "No sensitive information detected.",
        "No action required.",
        0
    ),

    "password": RiskResult(
        "password", 0, 100,
        "Critical",
        "Password detected in clipboard.",
        "Clear clipboard immediately.",
        15
    ),

    "api_key": RiskResult(
        "api_key", 0, 95,
        "Critical",
        "API key detected.",
        "Clipboard will be cleared.",
        15
    ),

    "jwt": RiskResult(
        "jwt", 0, 95,
        "Critical",
        "JWT token detected.",
        "Clipboard will be cleared.",
        20
    ),

    "ssh_key": RiskResult(
        "ssh_key", 0, 100,
        "Critical",
        "SSH Private Key detected.",
        "Clipboard will be cleared.",
        10
    ),

    "db_credentials": RiskResult(
        "db_credentials", 0, 90,
        "High",
        "Database credentials detected.",
        "Clipboard will be cleared.",
        20
    ),

    "payment": RiskResult(
        "payment", 0, 90,
        "High",
        "Payment information detected.",
        "Clipboard will be cleared.",
        20
    ),

    "otp": RiskResult(
        "otp", 0, 70,
        "Medium",
        "One-Time Password detected.",
        "Clipboard will be cleared after timeout.",
        30
    ),
}


def calculate_risk(category: str, confidence: float):

    result = RISK_TABLE[category]

    return RiskResult(
        category=result.category,
        confidence=confidence,
        risk_score=result.risk_score,
        risk_level=result.risk_level,
        explanation=result.explanation,
        action=result.action,
        timeout=result.timeout,
    )