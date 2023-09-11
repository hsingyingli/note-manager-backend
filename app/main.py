from fastapi import FastAPI
from config import lifespan
from app.routes import router
#
app = FastAPI(lifespan=lifespan)
app.include_router(router)
