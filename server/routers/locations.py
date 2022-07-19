from ..conn import *
from fastapi import APIRouter
from model.location import *

router = APIRouter()

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
