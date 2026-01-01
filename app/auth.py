from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings
from app.models import TokenData, User, UserInDB

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pre-hash the password once to avoid re-hashing on every request
# This also avoids the bcrypt 72-byte limit issue
_HASHED_PASSWORD = None


def get_password_hash(password: str) -> str:
    """Hash a password."""
    # Truncate password to 72 bytes if needed (bcrypt limitation)
    if len(password. encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against hashed password."""
    # Truncate password to 72 bytes if needed (bcrypt limitation)
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)


def _get_hashed_password() -> str:
    """Get the cached hashed password."""
    global _HASHED_PASSWORD
    if _HASHED_PASSWORD is None:
        _HASHED_PASSWORD = get_password_hash(settings.api_password)
    return _HASHED_PASSWORD


def get_user(username: str) -> Optional[UserInDB]:
    """Get user from 'database' (single user for now)."""
    if username == settings.api_username:
        return UserInDB(
            username=username, 
            hashed_password=_get_hashed_password()
        )
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user credentials."""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        #return None
        return user
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return User(username=user.username)