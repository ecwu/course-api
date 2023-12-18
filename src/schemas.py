from pydantic import BaseModel, EmailStr, HttpUrl
import datetime

from src.models import CourseLecturer


class CourseDescriptionBase(BaseModel):
    course_description: str


class CourseDescriptionCreate(CourseDescriptionBase):
    pass


class CourseDescription(CourseDescriptionBase):
    id: int
    course_id: int
    create_time: datetime.datetime

    class Config:
        from_attributes = True


class CourseNoteBase(BaseModel):
    course_note: str


class CourseNoteCreate(CourseNoteBase):
    pass


class CourseNote(CourseNoteBase):
    id: int
    course_id: int
    create_time: datetime.datetime

    class Config:
        from_attributes = True


class LecturerBase(BaseModel):
    name: str
    note: str = ''
    homepage: str = "https://staff.uic.edu.cn"
    email: str = "placeholder@uic.edu.cn"


class LecturerCreate(LecturerBase):
    pass


class Lecturer(LecturerBase):
    id: int
    edit_time: datetime.datetime

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    course_code: str
    course_name: str
    course_name_cn: str = ''
    course_units: int = 3
    course_type: str | None = None
    course_prerequisite: str | None = None
    visibility: bool = True


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int
    course_descriptions: list[CourseDescription] = []
    course_notes: list[CourseNote] = []
    update_time: datetime.datetime

    class Config:
        from_attributes = True


class TermBase(BaseModel):
    display_name: str
    year: int = 2005
    start_month: int = 9


class TermCreate(TermBase):
    pass


class Term(TermBase):
    id: int

    class Config:
        from_attributes = True
