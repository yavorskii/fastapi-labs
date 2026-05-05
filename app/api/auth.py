from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from app.schemas.auth import UserCreate, Token, TokenData
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token, 
    SECRET_KEY, ALGORITHM
)
from app.repository.mongo_repo import MongoBookRepository
from app.database import db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=201)
async def register(user_in: UserCreate):
    repo = MongoBookRepository(db)
    existing_user = await repo.get_user(user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user_dict = {
        "username": user_in.username,
        "hashed_password": get_password_hash(user_in.password)
    }
    await repo.create_user(user_dict)
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    repo = MongoBookRepository(db)
    user = await repo.get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {
        "access_token": create_access_token({"sub": user["username"]}),
        "refresh_token": create_refresh_token({"sub": user["username"]}),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate refresh token")
    
    return {
        "access_token": create_access_token({"sub": username}),
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }