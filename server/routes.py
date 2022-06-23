from fastapi import APIRouter
from psycopg2 import connect, extras
from dotenv import dotenv_values
import os
from model.model import *

config = dotenv_values(".env")
database = config['DATABASE'] if config else os.environ.get('DATABASE')
user = config['USER'] if config else os.environ.get('USER')
password = config['PASSWORD'] if config else os.environ.get('PASSWORD')
host = config['HOST'] if config else os.environ.get('HOST')

router = APIRouter()

conn = connect(database=database, user=user, password=password, host=host)
cur = conn.cursor(cursor_factory=extras.RealDictCursor)

@router.get("/get-users", response_model=UsersResponse)
async def get_all_user():
    try:
        cur.execute("select * from users")
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-users-for-dashboard", response_model=UsersResponseForDashboard)
async def get_dashboard_users():
    try:
        cur.execute("select * from users")
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-locations", response_model=LocationResponse)
async def get_locations():
    try:
        cur.execute("select loc_name from locations")
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])


@router.get("/get-user/{user_name}", response_model=UserResponse)
async def get_user(user_name: str):
    try:
        cur.execute(
            "SELECT first_name, last_name, phone, email, date_of_birth, user_name, user_pass, user_desc FROM users WHERE user_name = %s", (user_name,))
        result = cur.fetchone()
        return {
            "data": result if cur.rowcount else None,
            "is_success": True,
            "message": "success"}
    except Exception as e:
        print('ERR: ', e.args[0])


@router.post("/register", response_model=ApiResponse)
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

@router.post("/update-password", response_model=ApiResponse)
async def update_password(req: UpdatePasswordRequest):
    try:
        is_success = True
        message = 'success'
        sql = "update users set user_pass = %s where user_name = %s"
        data = [req.user_pass, req.user_name,]
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

@router.post("/update-info", response_model=ApiResponse)
async def update_info(req: UpdateInfoRequest):
    try:
        is_success = True
        message = 'success'
        sql = "update users set first_name=%s, last_name=%s, phone=%s, email=%s, date_of_birth=%s where user_name = %s"
        data = [req.first_name, req.last_name, req.phone, req.email, req.date_of_birth, req.user_name,]
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

@router.get("/get-trips", response_model=TripResponse)
async def get_trips():
    try:
        sql = 'SELECT trip.id, locations.loc_name, bus.price_per_seat, trip.seat, trip.departure_date FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-buses", response_model=BusResponse)
async def get_buses():
    try:
        sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, bus.num_of_seat, bus.price_per_seat, bus.status FROM bus JOIN bus_type ON bus.type_id = bus_type.id'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/add-bus", response_model=ApiResponse)
async def add_bus(req: AddBusRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO bus (bus_name, price_per_seat, type_id, created_date) VALUES (%s,%s,%s,%s)"
        data = [req.name, req.price, req.type_id, req.created_date,]
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

@router.post("/update-bus", response_model=ApiResponse)
async def update_bus(req: UpdateBusRequest):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE bus SET price_per_seat=%s, status=%s WHERE id=%s"
        data = [req.price, req.status, req.bus_id,]
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
