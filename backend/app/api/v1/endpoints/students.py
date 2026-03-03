from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.student import Student
from app.schemas.student import StudentOut

router = APIRouter()


@router.get("/", response_model=list[StudentOut])
def list_students(
    class_code: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[Student]:
    query = db.query(Student)
    if class_code:
        query = query.filter(Student.class_code == class_code)
    return query.order_by(Student.student_code.asc()).all()
