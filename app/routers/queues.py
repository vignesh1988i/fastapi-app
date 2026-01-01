from fastapi import APIRouter, Depends, Path
from typing import Dict, Any
from app.auth import get_current_user
from app.models import User
from app.services.mq_client import mq_client

router = APIRouter(prefix="/qmgr", tags=["Queues"])


@router.get("/{qmgr_name}/queues", response_model=Dict[str, Any])
async def list_queues(
    qmgr_name: str = Path(..., description="Queue Manager name"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    List all queues for a queue manager. 
    
    Endpoint: GET /qmgr/{qmgr_name}/queues
    """
    return mq_client.list_queues(qmgr_name)


@router.get("/{qmgr_name}/queues/{queue_name}", response_model=Dict[str, Any])
async def get_queue(
    qmgr_name: str = Path(..., description="Queue Manager name"),
    queue_name: str = Path(..., description="Queue name"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get specific queue details.
    
    Endpoint: GET /qmgr/{qmgr_name}/queues/{queue_name}
    """
    return mq_client.get_queue(qmgr_name, queue_name)

@router.get("/{qmgr_name}/queues/{queue_name}/attributes", response_model=Dict[str, Any])
async def get_queue_attributes(
    qmgr_name: str = Path(..., description="Queue Manager name"),
    queue_name: str = Path(..., description="Queue name"),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get specific queue attributes using MQSC endpoint.
    
    Endpoint: POST {qmgr_name}/mqsc
    """
    return mq_client.get_queue_attributes(qmgr_name, queue_name, 'mqsc')