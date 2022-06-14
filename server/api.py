from fastapi import FastAPI
from psycopg2 import connect, extras
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
database = config['DATABASE'] if config else os.environ.get('DATABASE')
user = config['USER'] if config else os.environ.get('USER')
password = config['PASSWORD'] if config else os.environ.get('PASSWORD')
host = config['HOST'] if config else os.environ.get('HOST')

app = FastAPI()
conn = connect(database = database, user = user, password = password, host = host)
cur = conn.cursor(cursor_factory=extras.RealDictCursor)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/users")
async def get_all_user():
    try:
        cur.execute("select * from users")
        result = cur.fetchall()
        return { "data" : result }
    except Exception as e:
        print('ERR: ', e.args[0])