from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.score import Score
from app.models.student import Student
from app.services.risk import delay_risk_score

router = APIRouter()


def _student_metrics(db: Session) -> list[dict[str, float | int | str]]:
    rows = (
        db.query(Student.student_code, Score.credits, Score.total_score)
        .join(Score, Score.student_id == Student.id, isouter=True)
        .all()
    )

    agg: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {
            "weighted_sum": 0.0,
            "credits": 0,
            "failed_courses": 0,
        }
    )
    for student_code, credits, total_score in rows:
        if credits is None or total_score is None:
            continue
        agg[student_code]["weighted_sum"] += float(total_score) * int(credits)
        agg[student_code]["credits"] += int(credits)
        if float(total_score) < 5.0:
            agg[student_code]["failed_courses"] += 1

    all_codes = [code for (code,) in db.query(Student.student_code).all()]
    metrics: list[dict[str, float | int | str]] = []
    for code in all_codes:
        item = agg.get(code, {"weighted_sum": 0.0, "credits": 0, "failed_courses": 0})
        credits = int(item["credits"])
        gpa = round(float(item["weighted_sum"]) / credits, 2) if credits > 0 else 0.0
        credit_deficit = max(0, 24 - credits)
        risk = delay_risk_score(
            gpa=gpa,
            credit_deficit=credit_deficit,
            retake_count=int(item["failed_courses"]),
        )
        metrics.append(
            {
                "student_code": code,
                "gpa": gpa,
                "credits": credits,
                "credit_deficit": credit_deficit,
                "failed_courses": int(item["failed_courses"]),
                "risk": risk,
            }
        )

    return metrics


@router.get("/macro")
def macro_dashboard(db: Session = Depends(get_db)) -> dict:
    metrics = _student_metrics(db)
    student_count = len(metrics)
    if student_count == 0:
        return {
            "faculty_avg_gpa": 0.0,
            "on_time_grad_rate": 0.0,
            "high_risk_students": 0,
        }

    faculty_avg_gpa = round(sum(float(m["gpa"]) for m in metrics) / student_count, 2)
    on_time_count = sum(1 for m in metrics if int(m["credits"]) >= 24 and float(m["gpa"]) >= 5.0)
    high_risk_students = sum(1 for m in metrics if float(m["risk"]) >= 65.0)

    return {
        "faculty_avg_gpa": faculty_avg_gpa,
        "on_time_grad_rate": round(on_time_count / student_count, 4),
        "high_risk_students": high_risk_students,
    }


@router.get("/micro")
def micro_dashboard(db: Session = Depends(get_db)) -> dict:
    metrics = sorted(_student_metrics(db), key=lambda x: float(x["risk"]), reverse=True)

    red_flags = []
    for item in metrics[:5]:
        gpa = float(item["gpa"])
        credit_deficit = int(item["credit_deficit"])
        failed_courses = int(item["failed_courses"])

        if gpa < 5.0:
            reason = "GPA thấp (< 5.0)"
        elif credit_deficit > 0:
            reason = "Nợ tín chỉ"
        elif failed_courses > 0:
            reason = "Có môn dưới 5"
        else:
            reason = "Nguy cơ học vụ tổng hợp"

        red_flags.append(
            {
                "student_code": item["student_code"],
                "reason": reason,
                "risk": item["risk"],
            }
        )

    killer_subject_rows = (
        db.query(Score.course_code, func.avg(Score.total_score).label("avg_score"))
        .group_by(Score.course_code)
        .order_by(func.avg(Score.total_score).asc())
        .limit(3)
        .all()
    )

    return {
        "red_flags": red_flags,
        "killer_subjects": [row[0] for row in killer_subject_rows],
    }
