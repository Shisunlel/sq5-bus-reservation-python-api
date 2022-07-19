from ..conn import *
from fastapi import APIRouter
from model.user import *

router = APIRouter()

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