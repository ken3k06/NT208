from pydantic import BaseModel


class StudentOut(BaseModel):
    id: int
    student_code: str
    full_name: str
    class_code: str

    model_config = {"from_attributes": True}
