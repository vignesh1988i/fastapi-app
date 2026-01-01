from fastapi import APIRouter, Depends, Path
from typing import Dict, Any
from app.auth import get_current_user
from app.models import User
from app.services.mq_client import mq_client

router = APIRouter(prefix="/qmgr", tags=["Queue Manager"])


@router.get("/{qmgr_name}/status", response_model=Dict[str, Any])
async def get_qmgr_status(
    qmgr_name: str = Path(..., description="Queue Manager name"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get queue manager status.
    
    Endpoint: GET /qmgr/{qmgr_name}/status
    """
    return mq_client.get_qmgr_status(qmgr_name)