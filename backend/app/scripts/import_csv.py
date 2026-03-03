import csv
import io
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Score, Student, User
from app.models.user import UserRole
from app.services.security import hash_password

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)


def import_students(db: Session, path: Path) -> int:
    created = 0
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["student_code"].strip()
            existing = db.query(Student).filter(Student.student_code == code).first()
            if existing:
                existing.full_name = row["full_name"].strip()
                existing.class_code = row["class_code"].strip()
                continue
            db.add(
                Student(
                    student_code=code,
                    full_name=row["full_name"].strip(),
                    class_code=row["class_code"].strip(),
                )
            )
            created += 1
    db.commit()
    return created


def upsert_scores_from_csv_text(db: Session, csv_text: str) -> dict[str, int]:
    students = {s.student_code: s.id for s in db.query(Student).all()}
    created = 0
    updated = 0
    skipped = 0

    reader = csv.DictReader(io.StringIO(csv_text))
    required_cols = {"student_code", "semester", "course_code", "credits", "total_score"}
    if not reader.fieldnames or not required_cols.issubset(set(reader.fieldnames)):
        raise ValueError("CSV thiếu cột bắt buộc: student_code, semester, course_code, credits, total_score")

    for row in reader:
        code = row["student_code"].strip()
        student_id = students.get(code)
        if not student_id:
            skipped += 1
            continue

        semester = row["semester"].strip()
        course_code = row["course_code"].strip()

        try:
            credits = int(row["credits"])
            total_score = float(row["total_score"])
        except (TypeError, ValueError):
            skipped += 1
            continue

        exists = (
            db.query(Score)
            .filter(
                Score.student_id == student_id,
                Score.semester == semester,
                Score.course_code == course_code,
            )
            .first()
        )
        if exists:
            exists.credits = credits
            exists.total_score = total_score
            updated += 1
            continue

        db.add(
            Score(
                student_id=student_id,
                semester=semester,
                course_code=course_code,
                credits=credits,
                total_score=total_score,
            )
        )
        created += 1

    db.commit()
    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
    }


def import_scores(db: Session, path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        content = f.read()
    result = upsert_scores_from_csv_text(db, content)
    return result["created"] + result["updated"]


def seed_default_users(db: Session) -> int:
    seeds = [
        ("admin@uit.edu.vn", "Dean Admin", UserRole.ADMIN, "admin123"),
        ("advisor1@uit.edu.vn", "Advisor One", UserRole.ADVISOR, "advisor123"),
    ]
    created = 0
    for email, full_name, role, password in seeds:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            continue
        db.add(
            User(
                email=email,
                full_name=full_name,
                role=role,
                hashed_password=hash_password(password),
                is_active=True,
            )
        )
        created += 1
    db.commit()
    return created


def run() -> None:
    ensure_schema()
    db = SessionLocal()
    try:
        students_created = import_students(db, DATA_DIR / "students.csv")
        scores_created = import_scores(db, DATA_DIR / "scores.csv")
        users_created = seed_default_users(db)
        print(
            {
                "students_created_or_updated": students_created,
                "scores_created_or_updated": scores_created,
                "users_created": users_created,
                "students_total": db.query(Student).count(),
                "scores_total": db.query(Score).count(),
                "users_total": db.query(User).count(),
            }
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
