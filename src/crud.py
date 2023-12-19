from sqlalchemy.orm import Session

from . import models, schemas


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_course_code(db: Session, course_code: str):
    return db.query(models.Course).filter(models.Course.course_code == course_code).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def query_courses_with_coursecode(db: Session, code: str, skip: int = 0, limit: int = 100):
    return db.query(models.Course).filter(models.Course.course_code.contains(code)).offset(skip).limit(limit).all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(course_code=course.course_code,
                              course_name=course.course_name,
                              course_name_cn=course.course_name_cn,
                              course_units=course.course_units,
                              course_prerequisite=course.course_prerequisite,
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


def get_lecturers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lecturer).offset(skip).limit(limit).all()


def get_lecturer(db: Session, lecturer_id: int):
    return db.query(models.Lecturer).filter(models.Lecturer.id == lecturer_id).first()


def create_lecturer(db: Session, lecturer: schemas.LecturerCreate):
    db_lecturer = models.Lecturer(name=lecturer.name,
                                  note=lecturer.note,
                                  homepage=lecturer.homepage,
                                  email=lecturer.email)
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer


def get_terms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Term).offset(skip).limit(limit).all()


def create_course_lecturer(db: Session, course_lecturer: schemas.CourseLecturerCreate):
    db_cl = models.CourseLecturer(course_id=course_lecturer.course_id,
                                  lecturer_id=course_lecturer.lecturer_id)
    db.add(db_cl)
    db.commit()
    db.refresh(db_cl)
    return db_cl


def create_course_offering_term(db: Session, course_offering_term: schemas.CourseOfferingTermCreate):
    db_cot = models.CourseOfferingTerm(course_id=course_offering_term.course_id,
                                       term_id=course_offering_term.term_id)
    db.add(db_cot)
    db.commit()
    db.refresh(db_cot)
    return db_cot

