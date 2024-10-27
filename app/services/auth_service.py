from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.schemas.user_schema import UserCreate  # Updated import path for UserCreate
from app.database.database import get_db  # Import get_db from the database module
from app.models.user_model import User  # Import User from the models module
from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme  # Import constants from core/security

async def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return False
    return user

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def create_user(user: UserCreate, db: Session):
    db_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
