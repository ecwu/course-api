from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, index=True)
    course_name = Column(String)
    course_name_cn = Column(String, default='')
    course_units = Column(Integer, default=3)
    course_type = Column(String)
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_archived = Column(Boolean, default=False)
    visibility = Column(Boolean, default=True)

    course_descriptions = relationship("CourseDescription", back_populates="course")
    course_notes = relationship("CourseNote", back_populates="course")
    course_lecturers = relationship("CourseLecturer", back_populates="course")
    course_offer_terms = relationship("CourseOfferTerm", back_populates="course")


class CourseDescription(Base):
    __tablename__ = "course_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    course_description = Column(String)
    create_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    course_id = Column(Integer, ForeignKey(Course.id))

    course = relationship("Course", back_populates="course_descriptions")


class CourseNote(Base):
    __tablename__ = "course_notes"

    id = Column(Integer, primary_key=True, index=True)
    course_note = Column(String)
    create_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    course_id = Column(Integer, ForeignKey(Course.id))

    course = relationship("Course", back_populates="course_notes")


class Lecturer(Base):
    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    note = Column(String)
    homepage = Column(String)
    email = Column(String)
    edit_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    course_lecturers = relationship("CourseOffering", back_populates="lecturer")


class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String)
    year = Column(Integer)
    start_month = Column(Integer)

    course_offer_terms = relationship("CourseOfferTerm", back_populates="term")


class CourseLecturer(Base):
    __tablename__ = "course_lecturers"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey(Course.id))
    lecturer_id = Column(Integer, ForeignKey(Lecturer.id))

    course = relationship("Course", back_populates="course_lecturers")
    lecturer = relationship("Lecturer", back_populates="course_lecturers")


class CourseOfferingTerm(Base):
    __tablename__ = "course_offering_terms"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey(Course.id))
    term_id = Column(Integer, ForeignKey(Term.id))

    course = relationship("Course", back_populates="course_offer_terms")
    term = relationship("Term", back_populates="course_offer_terms")

