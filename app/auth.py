import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

# Custom exceptions for easy redirects
class AuthRedirectException(Exception):
    def __init__(self, redirect_url: str, message: Optional[str] = None):
        self.redirect_url = redirect_url
        self.message = message

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretjwtkeyforhireaiplatformdevelopment123!")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_optional(request: Request, db: Session = Depends(get_db)) -> Optional[models.User]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    if token.startswith("Bearer "):
        token = token[7:]
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None
        
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    user = get_current_user_optional(request, db)
    if not user:
        raise AuthRedirectException(redirect_url="/login", message="Please login first.")
    return user

def require_role(roles: list):
    def dependency(request: Request, user: models.User = Depends(get_current_user)):
        if user.role not in roles:
            raise AuthRedirectException(
                redirect_url="/?error=Unauthorized",
                message=f"Access denied. Required roles: {roles}"
            )
        return user
    return dependency

# Specific role shortcuts
def require_admin(request: Request, user: models.User = Depends(get_current_user)):
    if user.role != "admin":
        raise AuthRedirectException(redirect_url="/", message="Admin access required.")
    return user

def require_recruiter(request: Request, user: models.User = Depends(get_current_user)):
    if user.role != "recruiter":
        raise AuthRedirectException(redirect_url="/", message="Recruiter access required.")
    return user

def require_candidate(request: Request, user: models.User = Depends(get_current_user)):
    if user.role != "candidate":
        raise AuthRedirectException(redirect_url="/", message="Candidate access required.")
    return user
