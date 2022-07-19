from ..conn import *
from fastapi import APIRouter
from model.booking import *

router = APIRouter()

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

@router.get("/get-users-from-booking", response_model=UsersBookingResponse, tags=["Booking"])
def get_bookings():
    try:
        sql = 'SELECT DISTINCT user_id FROM booking order by 1'
        cur.execute(sql)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.get("/get-user-from-booking/{booking_id}", response_model=UserBookingResponse, tags=["Booking"])
def get_user_booking(booking_id: int):
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

@router.get("/get-user-booking/{user_id}", response_model=BookingsResponse, tags=["Booking"])
def get_bus_seat(user_id: int):
    try:
        sql = 'SELECT * FROM booking WHERE user_id = %s ORDER BY booking_date DESC'
        data = [user_id, ]
        cur.execute(sql, data)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])