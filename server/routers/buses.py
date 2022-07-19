from ..conn import *
from fastapi import APIRouter
from model.bus import *

router = APIRouter()

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

@router.get("/get-bus-location/{loc_name}", response_model=BusLocationResponse, tags=["Bus"])
def get_bus_location(loc_name: str):
    try:
        sql = 'SELECT bus.bus_name FROM bus JOIN locations ON bus.loc_id = locations.loc_id WHERE locations.loc_name = %s AND bus.status = 1 order by 1'
        data = [loc_name, ]
        cur.execute(sql, data)
        result = cur.fetchall()
        return {
            "data": result,
            "is_success": True,
            "message": "success"
        }
    except Exception as e:
        print('ERR: ', e.args[0])
