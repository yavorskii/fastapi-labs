from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.repository.mongo_repo import MongoBookRepository
from app.database import get_db
from app.schemas.auth import UserCreate, Token
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token,
    SECRET_KEY, ALGORITHM
)
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=201)
async def register(user_in: UserCreate, db = Depends(get_db)):
    repo = MongoBookRepository(db)
    existing_user = await repo.get_user(user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_data = {
        "username": user_in.username,
        "hashed_password": get_password_hash(user_in.password)
    }
    await repo.create_user(user_data)
    return {"msg": "User created"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    repo = MongoBookRepository(db)
    user = await repo.get_user(form_data.username)
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": create_access_token({"sub": user["username"]}),
        "refresh_token": create_refresh_token({"sub": user["username"]}),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
            
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    repo = MongoBookRepository(db)
    user = await repo.get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    return {
        "access_token": create_access_token({"sub": user["username"]}),
        "refresh_token": create_refresh_token({"sub": user["username"]}),
        "token_type": "bearer"
    }