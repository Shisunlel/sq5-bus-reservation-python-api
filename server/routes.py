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

@router.get("/get-users", response_model=UsersResponse, tags=["User"])
async def get_all_user():
    try:
        cur.execute("select * from users order by 1")
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-users-for-dashboard", response_model=UsersResponseForDashboard, tags=["User"])
async def get_dashboard_users():
    try:
        cur.execute("select * from users order by 1")
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-locations", response_model=LocationsResponse, tags=["Location"])
async def get_locations():
    try:
        cur.execute("select loc_id, loc_name from locations order by loc_id")
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])


@router.get("/get-user/{user_name}", response_model=UserResponse, tags=["User"])
async def get_user(user_name: str):
    try:
        cur.execute(
            "SELECT first_name, last_name, phone, email, date_of_birth, user_name, user_pass, role_name user_desc FROM users JOIN role ON users.role_id = role.id WHERE user_name = %s", (user_name,))
        result = cur.fetchone()
        return {
            "data": result if cur.rowcount else None,
            "is_success": True,
            "message": "success"}
    except Exception as e:
        print('ERR: ', e.args[0])


@router.post("/register", response_model=ApiResponse, tags=["User"])
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

@router.post("/update-password", response_model=ApiResponse, tags=["User"])
async def update_password(req: UpdatePasswordRequest):
    try:
        is_success = True
        message = 'success'
        sql = "update users set user_pass = %s where user_name = %s"
        data = [req.user_pass, req.user_name, ]
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

@router.post("/update-info", response_model=ApiResponse, tags=["User"])
async def update_info(req: UpdateInfoRequest):
    try:
        is_success = True
        message = 'success'
        sql = "update users set first_name=%s, last_name=%s, phone=%s, email=%s, date_of_birth=%s where user_name = %s"
        data = [req.first_name, req.last_name, req.phone, req.email, req.date_of_birth, req.user_name, ]
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

@router.get("/get-trips", response_model=TripsResponse, tags=["Trip"])
async def get_trips():
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price_per_seat, trip.seat, trip.departure_date, trip.departure_time FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id order by 1'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])
    
@router.get("/get-trip-by-id/{trip_id}", response_model=TripResponse, tags=["Trip"])
async def get_trip_by_id(trip_id: int):
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price_per_seat, trip.seat, trip.departure_date, trip.departure_time FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id where trip.id = %s order by 1'
        data = [trip_id, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-trips-by-loc-and-departure/{loc_id}/{date}", response_model=TripsResponse, tags=["Trip"])
async def get_trips_by_loc_and_departure(loc_id: int, date: date):
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price_per_seat, trip.seat, trip.departure_date, trip.departure_time FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id where trip.loc_id = %s and trip.departure_date = %s order by 1'
        data = [loc_id, date, ]
        cur.execute(sql, data)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-buses", response_model=BusesResponse, tags=["Bus"])
async def get_buses():
    try:
        sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, bus.num_of_seat, bus.price_per_seat, bus.status FROM bus JOIN bus_type ON bus.type_id = bus_type.id order by 1'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-bus-by-name/{bus_name}", response_model=BusResponse, tags=["Bus"])
async def get_location_by_name(bus_name: str):
    try:
        sql = 'SELECT * FROM bus where bus_name = %s order by 1'
        data = [bus_name, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/add-bus", response_model=ApiResponse, tags=["Bus"])
async def add_bus(req: AddBusRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO bus (bus_name, price_per_seat, type_id, created_date) VALUES (%s,%s,%s,%s)"
        data = [req.name, req.price, req.type_id, req.created_date, ]
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

@router.post("/update-bus", response_model=ApiResponse, tags=["Bus"])
async def update_bus(req: UpdateBusRequest):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE bus SET price_per_seat=%s, status=%s WHERE id=%s"
        data = [req.price, req.status, req.bus_id, ]
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

@router.post("/update-user", response_model=ApiResponse, tags=["User"])
async def update_user(req: UpdateUserRequest):
    try:
        is_success = True
        message = 'success'
        role = "select id from role where role_name = %s"
        role_req = [req.user_role]
        cur.execute(role, role_req)
        role_data = cur.fetchone()
        sql = "update users set user_pass= %s, phone=%s, email=%s, role_id=%s where user_name = %s"
        data = [req.user_pass, req.phone, req.email, role_data['id'], req.user_name, ]
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

@router.post("/delete-user", response_model=ApiResponse, tags=["User"])
async def remove_user(req: DeleteUserRequest):
    try:
        is_success = True
        message = 'success'
        sql = "DELETE FROM users where user_name = %s"
        data = [req.user_name, ]
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

@router.get("/get-location-by-name/{loc_name}", response_model=LocationResponse, tags=["Location"])
async def get_location_by_name(loc_name: str):
    try:
        sql = 'SELECT loc_id, loc_name FROM locations where loc_name = %s order by 1'
        data = [loc_name, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/add-trip", response_model=ApiResponse, tags=["Trip"])
async def add_trip(req: AddTripRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO trip(loc_id, bus_id, departure_date, departure_time) VALUES (%s, %s, %s, %s)"
        data = [req.loc_id, req.bus_id, req.departure_date, req.departure_time, ]
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

@router.post("/update-trip", response_model=ApiResponse, tags=["Trip"])
async def update_trip(req: UpdateTripRequest):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE trip SET departure_date=%s, departure_time=%s WHERE id = %s"
        data = [req.departure_date, req.departure_time, req.trip_id, ]
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