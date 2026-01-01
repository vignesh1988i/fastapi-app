from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.config import get_settings
from app.models import Token
from app.auth import authenticate_user, create_access_token, get_current_user
from app.routers import qmgr, queues, channels
import json

settings = get_settings()
print(json.dumps(settings.dict(), indent=4))

app = FastAPI(
    title="IBM MQ Monitoring API",
    description="FastAPI wrapper for IBM MQ REST API with JWT authentication",
    version="1.0.0"
)

# Include routers
app.include_router(qmgr.router)
app.include_router(queues.router)
app.include_router(channels.router)


@app.post("/token", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint to get JWT access token.
    
    Use this token for all subsequent API calls.
    """
    user = authenticate_user(form_data. username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "IBM MQ Monitoring API",
        "version": "1.0. 0"
    }


@app.get("/protected", tags=["Test"])
async def protected_route(current_user: str = Depends(get_current_user)):
    """Test protected endpoint."""
    return {"message": f"Hello {current_user. username}!  You are authenticated."}