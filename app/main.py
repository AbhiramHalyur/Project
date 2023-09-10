from fastapi import FastAPI
from .routers import Employee,assets,dashboard



app = FastAPI() 

app.include_router(Employee.router)
app.include_router(assets.router)
app.include_router(dashboard.router)

