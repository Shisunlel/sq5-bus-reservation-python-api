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

@router.get("/get-bus-seat-id-by-trip/{seat_name}/{trip}", response_model=BusSeatIdResponse, tags=["BusSeat"])
def get_bus_seat(seat_name: int, trip: int):
    try:
        sql = 'SELECT id FROM bus_seat WHERE seat_name = %s AND bus_id IN (SELECT bus_id FROM trip WHERE id = %s)'
        data = [str(seat_name), trip, ]
        cur.execute(sql, data)
        result = cur.fetchone()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])

@router.post("/update-bus-seat-status", response_model=ApiResponse, tags=["BusSeat"])
def add_booking_detail(req: UpdateBusSeat):
    try:
        is_success = True
        message = 'success'
        sql = "UPDATE bus_seat SET status = %s WHERE id = %s"
        data = [req.status, req.seat_id, ]
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

@router.post("/add-booking-detail", response_model=ApiResponse, tags=["BookingDetail"])
def add_booking_detail(req: AddBookingDetailRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO booking_detail (booking_id, trip_id, seat_id, price) VALUES (%s, %s, %s, %s)"
        data = [req.booking_id, req.trip_id, req.seat_id, req.price ]
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

@router.post("/online-payment", response_model=ApiResponse, tags=["Transaction"])
def online_payment(req: AddOnlinePaymentRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO payment_online (booking_id, pay_date, cus_id) VALUES (%s, %s, %s)"
        data = [req.booking_id, req.pay_date, req.cus_id ]
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

@router.post("/offline-payment", response_model=ApiResponse, tags=["Transaction"])
def offline_payment(req: AddOfflinePaymentRequest):
    try:
        is_success = True
        message = 'success'
        sql = "INSERT INTO payment_offline (booking_id, booking_date, cus_id) VALUES (%s, %s, %s)"
        data = [req.booking_id, req.booking_date, req.cus_id ]
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

@router.get("/get-bus-seat-from-trip/{trip_id}", response_model=BusSeatsResponse, tags=["BusSeat"])
def get_bus_seat(trip_id: int):
    try:
        sql = 'SELECT * FROM bus_seat WHERE bus_id IN (SELECT bus_id FROM trip WHERE id=%s) order by 1'
        data = [trip_id, ]
        cur.execute(sql, data)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])