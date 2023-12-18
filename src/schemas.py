from pydantic import BaseModel, EmailStr, HttpUrl
import datetime


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
    note: str
    homepage: HttpUrl
    email: EmailStr


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
