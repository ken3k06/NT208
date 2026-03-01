from fastapi import APIRouter

from app.services.risk import delay_risk_score

router = APIRouter()


@router.get("/macro")
def macro_dashboard() -> dict:
    return {
        "faculty_avg_gpa": 7.15,
        "on_time_grad_rate": 0.74,
        "high_risk_students": 42,
    }


@router.get("/micro")
def micro_dashboard() -> dict:
    sample_risk = delay_risk_score(gpa=5.9, credit_deficit=12, retake_count=2)
    return {
        "red_flags": [
            {"student_code": "22520001", "reason": "GPA giảm > 1.5", "risk": sample_risk},
            {"student_code": "22520012", "reason": "Nợ tín chỉ", "risk": 68.5},
        ],
        "killer_subjects": ["NT208", "CS221", "MA102"],
    }
