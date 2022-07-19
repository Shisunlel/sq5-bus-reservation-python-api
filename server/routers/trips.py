from ..conn import *
from fastapi import APIRouter
from model.trip import *

router = APIRouter()

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
