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
def read_courses(code: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if code:
        courses = crud.query_courses_with_coursecode(db, code=code, skip=skip, limit=limit)
    else:
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


@app.post("/lecturers/", response_model=schemas.Lecturer)
def create_lecturer(lecturer: schemas.LecturerCreate, db: Session = Depends(get_db)):
    return crud.create_lecturer(db=db, lecturer=lecturer)


@app.get("/lecturers/", response_model=list[schemas.Lecturer])
def read_lecturers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lecturers = crud.get_lecturers(db, skip=skip, limit=limit)
    return lecturers


@app.get("/lecturers/{lecturer_id}", response_model=schemas.Lecturer)
def read_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    lecturer = crud.get_lecturer(db, lecturer_id=lecturer_id)
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return lecturer


@app.post("/terms/", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    return crud.create_term(db=db, term=term)


@app.get("/terms/", response_model=list[schemas.Term])
def read_terms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terms = crud.get_terms(db, skip=skip, limit=limit)
    return terms
