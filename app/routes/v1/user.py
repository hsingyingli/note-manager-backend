from fastapi import APIRouter

user_router = APIRouter()

def index():
    return {"message": 'hello world api route'}

@user_router.get('/')
def get_user():
    return {}
