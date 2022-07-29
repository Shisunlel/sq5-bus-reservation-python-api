from typing import NewType
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
        if not result:
            return {
                "data": None,
                "status": True,
                "message": "Not Found!"
            }
        else:
            res = list()
            booking = list()

            for x in result:
                booking.append(x)

            for x in booking:
                seat = list()
                sql = 'SELECT * FROM bus_seat WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s) order by 1'
                data = [x['id'], ]
                cur.execute(sql, data)
                result = cur.fetchall()

                for y in result:
                    seat.append(y['seat_name'])
                sql = 'SELECT DISTINCT trip_id FROM booking_detail WHERE booking_id = %s order by 1'
                data = [x['id'], ]
                cur.execute(sql, data)

                trip = cur.fetchone()

                sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, bus.price, trip.seat, trip.departure_date, trip.departure_time, trip.status FROM trip JOIN locations ON trip.loc_id = locations.loc_id JOIN bus ON trip.bus_id = bus.id where trip.id = %s order by 1'
                data = [trip['trip_id'], ]
                cur.execute(sql, data)
                booking_detail = cur.fetchone()

                res.append(
                    {
                        "booking_id": str(x['id']),
                        "trip_id": str(trip['trip_id']),
                        "destination": booking_detail['loc_name'],
                        "booking_date": str(x['booking_date']),
                        "price": str(x['payment']),
                        "bus_name": booking_detail['bus_name'],
                        "seat": ",".join(seat),
                        "paid_status": "Paid" if x['status'] == 1 else "Not Paid",
                    }
                )
            result = res
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/add-booking", response_model=AddBookingResponse, tags=["Booking"])
def add_booking(req: AddBookingRequest):
    try:
        is_success = True
        message = 'success'
        sql = 'INSERT INTO booking (user_id, payment, booking_date) VALUES (%s, %s, %s) RETURNING id'
        data = [req.user_id, req.payment, req.booking_date, ]
        cur.execute(sql, data)
        if cur.rowcount:
            conn.commit()
        else:
            is_success = False
            message = 'fail'
        id = cur.fetchone()['id']
        return {
            "data": id,
            "is_success": is_success,
            "message": message
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/update-booking-status", response_model=ApiResponse, tags=["Booking"])
def update_booking_status(req: UpdateBookingStatus):
    try:
        is_success = True
        message = 'success'
        sql = 'UPDATE booking SET status = %s WHERE id = %s'
        data = [req.status, req.booking_id, ]
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