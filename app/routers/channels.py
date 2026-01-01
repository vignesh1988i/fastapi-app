from fastapi import APIRouter, Depends, Path
from typing import Dict, Any
from app. auth import get_current_user
from app.models import User
from app.services.mq_client import mq_client

router = APIRouter(prefix="/qmgr", tags=["Channels"])


@router.get("/{qmgr_name}/channels", response_model=Dict[str, Any])
async def list_channels(
    qmgr_name: str = Path(..., description="Queue Manager name"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    List all channels for a queue manager.
    
    Endpoint: GET /qmgr/{qmgr_name}/channels
    """
    return mq_client.list_channels(qmgr_name)


@router.get("/{qmgr_name}/channels/{channel_name}", response_model=Dict[str, Any])
async def get_channel(
    qmgr_name: str = Path(..., description="Queue Manager name"),
    channel_name: str = Path(..., description="Channel name"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get specific channel details.
    
    Endpoint: GET /qmgr/{qmgr_name}/channels/{channel_name}
    """
    return mq_client.get_channel(qmgr_name, channel_name)