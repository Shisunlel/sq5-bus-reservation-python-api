from fastapi import FastAPI
from psycopg2 import connect, extras

app = FastAPI()
conn = connect(database="rwmprcfu", user="rwmprcfu", password="PMATMochoBaVnxc9UvDabt-dk8KDcEIQ", host="arjuna.db.elephantsql.com")
cur = conn.cursor(cursor_factory=extras.RealDictCursor)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/users")
async def get_all_user():
    try:
        cur.execute("select * from pro_user")
        result = cur.fetchall()
        return { "data" : result }
    except Exception as e:
        print('ERR: ', e.args[0])