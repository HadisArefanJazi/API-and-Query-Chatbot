 
# an API is a way for one program to communicate with another program.
# API means application programming interface.

# a chatbot is a program that talks with the user.
# in this project, the chatbot asks the api for data.

# simple flow:
# user -> chatbot -> api -> data
# data -> api -> chatbot -> user

# fastapi is a python framework for building apis.
# uvicorn is the server that runs the fastapi app.

from fastapi import FastAPI


# ============================================================
# 1. create the api app
# ============================================================

# app is the main fastapi object.
# uvicorn will run this object.

app = FastAPI()

# ============================================================
# 2. sample data
# ============================================================

# this dictionary stores student enrollment data.
# the key is the year.
# the value is the number of students.

data = {
    2024: 1700,
    2025: 1650,
    2026: 1800
}


# ============================================================
# 3. home endpoint
# ============================================================

# @app.get("/") creates a get endpoint.
# get means the client wants to read data.
# "/" is the home path.
# when the user opens http://127.0.0.1:8000/
# this function runs.

@app.get("/")
def home():
    return {"message": "api is running"}


# ============================================================
# 4. get all enrollment data
# ============================================================

# this endpoint returns the whole dictionary.

@app.get("/students")
def get_all_students():
    return data


# ============================================================
# 5. get enrollment by year
# ============================================================

# this endpoint receives a year from the user.
# example:
# http://127.0.0.1:8000/students/enrollment?year=2025

# year: int means fastapi expects year to be an integer.
# data.get(year) safely looks for the year in the dictionary.
# if the year does not exist, it returns none.

@app.get("/students/enrollment")
def get_enrollment(year: int):

    students = data.get(year)

    if students is None:
        return {
            "year": year,
            "error": "no data for this year"
        }

    return {
        "year": year,
        "students": students
    }


# ============================================================
# 6. post example
# ============================================================

# post means create new data.
# this endpoint receives json data from the client.
# example json:
# {
#     "year": 2027,
#     "students": 1900
# }

@app.post("/students/enrollment")
def add_enrollment(item: dict):

    year     = item.get("year")
    students = item.get("students")

    if year is None or students is None:
        return {"error": "please provide year and students"}

    data[year] = students

    return {
        "message": "new enrollment added",
        "data": data
    }


# ============================================================
# 7. put example
# ============================================================

# put means update existing data.
# this endpoint updates the number of students for a year.

@app.put("/students/enrollment/{year}")
def update_enrollment(year: int, item: dict):

    students = item.get("students")

    if students is None:
        return {"error": "please provide students"}

    if year not in data:
        return {"error": "year not found"}

    data[year] = students

    return {
        "message": "enrollment updated",
        "year": year,
        "students": students
    }


# ============================================================
# 8. delete example
# ============================================================

# delete means remove data.
# this endpoint removes one year from the dictionary.

@app.delete("/students/enrollment/{year}")
def delete_enrollment(year: int):

    if year not in data:
        return {"error": "year not found"}

    removed_value = data.pop(year)

    return {
        "message": "enrollment deleted",
        "year": year,
        "students": removed_value
    }


# ============================================================
# 9. how to run this api
# ============================================================

# in terminal, run:
# uvicorn api_chatbot:app --reload

# meaning:
# api_chatbot = this is our file name without .py
# app         = the fastapi object
# --reload    = restart automatically after code changes

# then open:
# http://127.0.0.1:8000/docs

# /docs gives an automatic testing page.


# ============================================================
# summary
# ============================================================

# api        -> communication system between programs
# request    -> question sent to the api
# response   -> answer returned by the api
# endpoint   -> url path such as /students
# json       -> common data format for api responses
# get        -> read data
# post       -> create data
# put        -> update data
# delete     -> remove data
# fastapi    -> python tool for building apis
# uvicorn    -> server that runs the api
 
