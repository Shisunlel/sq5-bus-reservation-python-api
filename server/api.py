from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import routes, users, bookings, buses, locations, trips


app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.include_router(users.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(buses.router, prefix="/api/v1")
app.include_router(locations.router, prefix="/api/v1")
app.include_router(trips.router, prefix="/api/v1")
app.include_router(routes.router, prefix="/api/v1")