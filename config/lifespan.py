from fastapi import FastAPI
from contextlib import asynccontextmanager

# configure life span
@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start
    print('start app')
    yield
    # after app end
    print('end app')
