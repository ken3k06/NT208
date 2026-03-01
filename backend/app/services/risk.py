def delay_risk_score(gpa: float, credit_deficit: int, retake_count: int) -> float:
    """Heuristic score in [0, 100]."""
    gpa_norm = min(max(gpa / 10.0, 0.0), 1.0)
    credit_penalty = min(max(credit_deficit / 30.0, 0.0), 1.0)
    retake_penalty = min(max(retake_count / 6.0, 0.0), 1.0)

    risk = (0.45 * (1.0 - gpa_norm)) + (0.35 * credit_penalty) + (0.20 * retake_penalty)
    return round(risk * 100, 2)
