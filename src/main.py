from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)


@app.get("/courses/", response_model=list[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@app.get("/courses/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.post("/courses/{course_id}/course_descriptions/", response_model=schemas.CourseDescription)
def create_description_for_course(
    course_id: int, course_description: schemas.CourseDescriptionCreate, db: Session = Depends(get_db)
):
    return crud.create_course_description(db=db, course_description=course_description, course_id=course_id)


@app.get("/course_descriptions/", response_model=list[schemas.CourseDescription])
def read_course_descriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    course_descriptions = crud.get_course_descriptions(db, skip=skip, limit=limit)
    return course_descriptions


@app.post("/courses/{course_id}/course_notes/", response_model=schemas.CourseNote)
def create_note_for_course(
    course_id: int, course_note: schemas.CourseNoteCreate, db: Session = Depends(get_db)
):
    return crud.create_course_note(db=db, course_note=course_note, course_id=course_id)


@app.get("/course_notes/", response_model=list[schemas.CourseNote])
def read_course_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    course_notes = crud.get_course_notes(db, skip=skip, limit=limit)
    return course_notes


@app.get("/lecturer/", response_model=list[schemas.Lecturer])
def read_lecturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lecturers = crud.get_lecturer(db, skip=skip, limit=limit)
    return lecturers
