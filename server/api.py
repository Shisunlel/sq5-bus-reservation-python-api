from fastapi import FastAPI
from psycopg2 import connect, extras
from dotenv import dotenv_values
import os
from fastapi.middleware.cors import CORSMiddleware
from model.model import *

config = dotenv_values(".env")
database = config['DATABASE'] if config else os.environ.get('DATABASE')
user = config['USER'] if config else os.environ.get('USER')
password = config['PASSWORD'] if config else os.environ.get('PASSWORD')
host = config['HOST'] if config else os.environ.get('HOST')

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
conn = connect(database=database, user=user, password=password, host=host)
cur = conn.cursor(cursor_factory=extras.RealDictCursor)

@app.get("/get-users", response_model=UsersResponse)
async def get_all_user():
    try:
        cur.execute("select * from users")
        result = cur.fetchall()
        return {"data": {
            "users": result, },
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])


@app.get("/get-locations", response_model=LocationResponse)
async def get_locations():
    try:
        cur.execute("select loc_name from locations")
        result = cur.fetchall()
        return {"data": {
            "locations": result,
        },
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])


@app.get("/get-user/{user_name}", response_model=UserResponse)
async def get_user(user_name: str):
    try:
        cur.execute(
            "SELECT first_name, last_name, phone, email, date_of_birth, user_name, user_pass, user_desc FROM users WHERE user_name = %s", (user_name,))
        result = cur.fetchone()
        return {"data": {
            "user": result,
        }, "is_success": True,
            "message": "success"}
    except Exception as e:
        print('ERR: ', e.args[0])


@app.post("/register", response_model=ApiResponse)
async def register(req: RegisterModel):
    try:
        is_success = True
        message = 'success'
        sql = "insert into users (user_name, user_pass, email)  values (%s, %s, %s)"
        data = [req.user_name, req.user_pass, req.email, ]
        cur.execute(sql, data)
        if cur.rowcount:
            conn.commit()
        else:
            is_success = False
            message = 'fail'
        return {
            "data": None,
            "is_success": is_success,
            "message": message
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@app.post("/update-password", response_model=ApiResponse)
async def update_password(user_pass: str, user_name: str):
    try:
        is_success = True
        message = 'success'
        sql = "update users set user_pass = %s where user_name = %s"
        data = [user_pass, user_name,]
        cur.execute(sql, data)
        if cur.rowcount:
            conn.commit()
        else:
            is_success = False
            message = 'fail'
        return {
            "data": None,
            "is_success": is_success,
            "message": message
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@app.post("/update-info", response_model=ApiResponse)
async def update_info(req: UpdateInfoRequest, user_name: str):
    try:
        is_success = True
        message = 'success'
        sql = "update users set first_name=%s, last_name=%s, phone=%s, email=%s, date_of_birth=%s where user_name = %s"
        data = [req.first_name, req.last_name, req.phone, req.email, req.date_of_birth, user_name,]
        cur.execute(sql, data)
        if cur.rowcount:
            conn.commit()
        else:
            is_success = False
            message = 'fail'
        return {
            "data": None,
            "is_success": is_success,
            "message": message
        }
    except Exception as e:
        print('ERR: ', e.args[0])