from datetime import date
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from huggingface_hub import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Book, Patient
from app.settings import DATABASE_URL

# DISCLAIMER:
# This is a very simple CRUD API
# Not intended for production


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


@app.post("/patient")
def create_patient(name: str, age: int, gender: str):
    session = Session()
    patient = Patient(name=name, age=age, gender=gender)
    session.add(patient)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


@app.get("/patients/{id}")
def find_patient(id: int):
    session = Session()
    patient = session.query(Patient).filter(Patient.id == id).first()
    session.close()

    result = jsonable_encoder({"patient": patient})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@app.get("/patients")
def get_patients(page_size: int = 10, page: int = 1):
    if page_size > 100 or page_size < 0:
        page_size = 100

    session = Session()
    patients = session.query(Patient).limit(page_size).offset((page - 1) * page_size).all()
    session.close()

    result = jsonable_encoder({"patients": patients})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@app.put("/patients")
def update_patient(id: int, name: Optional[str] = None, age: Optional[int] = None, gender: Optional[str] = None):
    session = Session()
    patient = session.query(Patient).get(id)
    if name is not None:
        patient.name = name
    if age is not None:
        patient.age = age
    if gender is not None:
        patient.gender = gender
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


@app.delete("/patients")
def delete_patient(id: int):
    session = Session()
    patient = session.query(Patient).get(id)
    session.delete(patient)
    session.commit()
    session.close()

    return JSONResponse(
        status_code=200, content={"status_code": 200, "message": "success"}
    )


@app.exception_handler(Exception)
def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(
        status_code=status_code,
        content={"status_code": status_code, "message": message},
    )
