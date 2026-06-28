 
# an API is a way for one program to communicate with another program.
# API means application programming interface.

# a chatbot is a program that talks with the user.
# in this project, the chatbot asks the api for data.

# simple flow:
# user -> chatbot -> api -> data
# data -> api -> chatbot -> user



import argparse
import re

import requests
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Student Enrollment Data API")

enrollment_data = {
    2024: 1700,
    2025: 1650,
    2026: 1800
}


class EnrollmentRecord(BaseModel):
    year: int
    students: int


class EnrollmentUpdate(BaseModel):
    students: int


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/students")
def get_all_students():
    return [
        {"year": year, "students": students}
        for year, students in sorted(enrollment_data.items())
    ]


@app.get("/students/enrollment")
def get_enrollment(year: int):
    if year not in enrollment_data:
        raise HTTPException(status_code=404, detail="No data for this year")

    return {
        "year": year,
        "students": enrollment_data[year]
    }


@app.post("/students/enrollment")
def add_enrollment(record: EnrollmentRecord):
    if record.year in enrollment_data:
        raise HTTPException(status_code=409, detail="Year already exists")

    enrollment_data[record.year] = record.students

    return {
        "message": "Enrollment record added",
        "year": record.year,
        "students": record.students
    }


@app.put("/students/enrollment/{year}")
def update_enrollment(year: int, record: EnrollmentUpdate):
    if year not in enrollment_data:
        raise HTTPException(status_code=404, detail="Year not found")

    enrollment_data[year] = record.students

    return {
        "message": "Enrollment record updated",
        "year": year,
        "students": record.students
    }


@app.delete("/students/enrollment/{year}")
def delete_enrollment(year: int):
    if year not in enrollment_data:
        raise HTTPException(status_code=404, detail="Year not found")

    students = enrollment_data.pop(year)

    return {
        "message": "Enrollment record deleted",
        "year": year,
        "students": students
    }


def find_year(question):
    matches = re.findall(r"\b\d{4}\b", question)

    if not matches:
        return None

    return int(matches[-1])


def ask_api(year):
    api_url = "http://127.0.0.1:8000/students/enrollment"

    try:
        response = requests.get(
            api_url,
            params={"year": year},
            timeout=10
        )

        if response.status_code == 404:
            return {"error": response.json().get("detail", "No data found")}

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:
        return {"error": "Could not connect to the API"}


def run_chatbot():
    question = input("Ask me: ")

    year = find_year(question)

    if year is None:
        print("Please include a year.")
        return

    result = ask_api(year)

    if "error" in result:
        print(result["error"])
        return

    print(f"{result['students']} students enrolled in {result['year']}.")


def run_api():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["api", "chatbot"])
    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    else:
        run_chatbot()


if __name__ == "__main__":
    main()
 
