from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import router as db_router, create_db_and_tables
from app.models.auth.api import router as auth_router
from app.models.users.api import router as users_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Либо укажи конкретный адрес, например ["http://127.0.0.1:5500"]
    allow_credentials=True, # ВАЖНО: разрешает передачу кук и заголовков авторизации
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(db_router)
app.include_router(auth_router)
app.include_router(users_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.on_event("shutdown")
async def shutdown_event():
    shutdown_event()

@app.get("/")
async def root():
    return {"message": "Welcome to the home endpoint!"}

