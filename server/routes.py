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
def get_all_user():
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
def get_dashboard_users():
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
def get_locations():
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
def get_user(user_name: str):
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
def register(req: RegisterModel):
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
def update_password(req: UpdatePasswordRequest):
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
def update_info(req: UpdateInfoRequest):
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
def get_trips():
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price, trip.seat, trip.departure_date, trip.departure_time, trip.status FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id order by 1'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-active-trips", response_model=TripsResponse, tags=["Trip"])
def get_active_trips():
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price, trip.seat, trip.departure_date, trip.departure_time, trip.status FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id WHERE trip.status = 1 order by 1'
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
def get_trip_by_id(trip_id: int):
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price, trip.seat, trip.departure_date, trip.departure_time, trip.status FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id where trip.id = %s order by 1'
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
def get_trips_by_loc_and_departure(loc_id: int, date: date):
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price, trip.seat, trip.departure_date, trip.departure_time FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id where trip.loc_id = %s and trip.departure_date = %s order by 1'
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
def get_buses():
    try:
        sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, bus.num_of_seat, bus.price, bus.status FROM bus JOIN bus_type ON bus.type_id = bus_type.id order by 1'
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
def get_location_by_name(bus_name: str):
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
def add_bus(req: AddBusRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO bus (bus_name, price, type_id, loc_id, created_date) VALUES (%s,%s,%s,%s, %s)"
        data = [req.name, req.price, req.type_id, req.loc_id, req.created_date, ]
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
def update_bus(req: UpdateBusRequest):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE bus SET price=%s, status=%s WHERE id=%s"
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
def update_user(req: UpdateUserRequest):
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
def remove_user(req: DeleteUserRequest):
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
def get_location_by_name(loc_name: str):
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
def add_trip(req: AddTripRequest):
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
def update_trip(req: UpdateTripRequest):
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

@router.post("/end-trip", response_model=ApiResponse, tags=["Trip"])
def end_trip(req: EndTripRequest):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE trip, bus SET trip.status = 0, bus.status = 1 WHERE trip.id = %s AND trip.bus_id = bus.id"
        data = [req.trip_id, ]
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

@router.get("/get-bookings", response_model=BookingsResponse, tags=["Booking"])
def get_bookings():
    try:
        sql = 'SELECT * FROM booking order by 1'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-booking-by-id/{booking_id}", response_model=BookingResponse, tags=["Booking"])
def get_booking_by_id(booking_id: int):
    try:
        sql = 'SELECT * FROM booking WHERE id = %s order by 1'
        data = [booking_id, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-bus-seat-from-booking/{booking_id}", response_model=BusSeatsResponse, tags=["BusSeat"])
def get_bus_seat(booking_id: int):
    try:
        sql = 'SELECT * FROM bus_seat WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s) order by 1'
        data = [booking_id, ]
        cur.execute(sql, data)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-trip-id-from-booking/{booking_id}", response_model=BookingDetailResponse, tags=["BookingDetail"])
def get_bus_seat(booking_id: int):
    try:
        sql = 'SELECT DISTINCT * FROM booking_detail WHERE booking_id = %s order by 1'
        data = [booking_id, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-user-from-booking/{booking_id}", response_model=UserResponse, tags=["User"])
def get_bus_seat(booking_id: int):
    try:
        sql = 'SELECT users.user_name FROM booking JOIN users ON booking.user_id = users.user_id WHERE booking.id = %s order by 1'
        data = [booking_id, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/update-transaction", response_model=ApiResponse, tags=["Transaction"])
def update_transaction(req: UpdateTransactionRequest):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE booking, payment_offline SET booking.status= 1, payment_offline.status = 1 WHERE booking.id = %s AND payment_offline.booking_id = %s"
        data = [req.booking_id, req.booking_id, ]
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

@router.get("/get-active-buses", response_model=BusesResponse, tags=["Bus"])
def get_active_buses():
    try:
        sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, bus.num_of_seat, bus.price, bus.status FROM bus JOIN bus_type ON bus.type_id = bus_type.id WHERE status = 1 order by 1'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])