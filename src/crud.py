from sqlalchemy.orm import Session

from . import models, schemas


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_course_code(db: Session, course_code: str):
    return db.query(models.Course).filter(models.Course.course_code == course_code).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(course_code=course.course_code,
                              course_name=course.course_name,
                              course_name_cn=course.course_name_cn,
                              course_units=course.course_units,
                              course_type=course.course_type)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_course_descriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CourseDescription).offset(skip).limit(limit).all()


def create_course_description(db: Session, course_description: schemas.CourseDescriptionCreate, course_id: int):
    db_cd = models.CourseDescription(**course_description.dict(), course_id=course_id)
    db.add(db_cd)
    db.commit()
    db.refresh(db_cd)
    return db_cd


def get_course_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CourseNote).offset(skip).limit(limit).all()


def create_course_note(db: Session, course_note: schemas.CourseNoteCreate, course_id: int):
    db_cn = models.CourseNote(**course_note.dict(), course_id=course_id)
    db.add(db_cn)
    db.commit()
    db.refresh(db_cn)
    return db_cn


def get_lecturer(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lecturer).offset(skip).limit(limit).all()