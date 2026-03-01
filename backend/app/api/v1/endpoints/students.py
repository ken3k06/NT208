from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_students() -> list[dict]:
    return [
        {"id": 1, "student_code": "22520001", "full_name": "Nguyen Van A", "class_code": "ATTT2023.1"},
        {"id": 2, "student_code": "22520002", "full_name": "Tran Thi B", "class_code": "ATTT2023.1"},
    ]
