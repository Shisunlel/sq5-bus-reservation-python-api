from ..conn import *
from fastapi import APIRouter

router = APIRouter()

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

@router.get("/get-trip-id-from-booking/{booking_id}", response_model=BookingDetailTripResponse, tags=["BookingDetail"])
def get_trip_id_booking(booking_id: int):
    try:
        sql = 'SELECT DISTINCT trip_id FROM booking_detail WHERE booking_id = %s order by 1'
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
