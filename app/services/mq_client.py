import requests
from typing import Dict, Any, Optional
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException, status
from app.config import get_settings

settings = get_settings()


class MQClient:
    """IBM MQ REST API Client."""
    
    def __init__(self):
        self.base_url = settings.mq_rest_base_url
        self.base_mqsc_url = settings.mq_rest_base_mqsc_url
        self.auth = HTTPBasicAuth(settings.mq_username, settings.mq_password)
        self.headers = {
            "Content-Type": "application/json",
            "ibm-mq-rest-csrf-token": ""  # Required for MQ REST API
        }
        # Disable SSL warnings for development (no SSL configured)
        requests.packages.urllib3.disable_warnings()
    
    def _make_request(self, endpoint: str, method: str = "GET") -> Dict[str, Any]:
        """Make HTTP request to MQ REST API."""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                headers=self.headers,
                verify=False,  # No SSL verification
                timeout=10
            )
            
            # Handle different response status codes
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            elif response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resource not found: {endpoint}"
                )
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="MQ authentication failed.  Check MQ credentials."
                )
            elif response.status_code == 403:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access forbidden. Check MQ user permissions."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"MQ REST API error: {response.status_code} - {response.text}"
                )
                
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cannot connect to MQ REST API. Check if MQWEB is running."
            )
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="MQ REST API request timed out."
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
    
    def _make_mqsc_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP POST request to MQSC endpoint."""
        url = f"{self.base_mqsc_url}/{endpoint}"
        #print(f"MQSC Request URL: {url}")
        #print(f"MQSC Request Payload: {payload}")
        
        try:
            response = requests.post(
                url=url,
                auth=self.auth,
                headers=self.headers,
                json=payload,
                verify=False,
                timeout=10
            )
            #print(f"MQSC Response Status Code: {response.status_code}")
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"MQSC request error: {response.status_code} - {response.text}"
                )
                
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cannot connect to MQ REST API. Check if MQWEB is running."
            )
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="MQ REST API request timed out."
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        

    def get_qmgr_status(self, qmgr_name: str) -> Dict[str, Any]:
        """Get queue manager status."""
        endpoint = f"qmgr/{qmgr_name}?status=*"
        return self._make_request(endpoint)
    
    def list_queues(self, qmgr_name: str) -> Dict[str, Any]:
        """List all queues for a queue manager."""
        endpoint = f"qmgr/{qmgr_name}/queue"
        return self._make_request(endpoint)
    
    def get_queue(self, qmgr_name: str, queue_name: str) -> Dict[str, Any]:
        """Get specific queue details."""
        endpoint = f"qmgr/{qmgr_name}/queue/{queue_name}"
        return self._make_request(endpoint)
    
    def list_channels(self, qmgr_name: str) -> Dict[str, Any]:
        """List all channels for a queue manager."""
        endpoint = f"qmgr/{qmgr_name}/channel"
        return self._make_request(endpoint)
    
    def get_channel(self, qmgr_name: str, channel_name: str) -> Dict[str, Any]:
        """Get specific channel details."""
        endpoint = f"qmgr/{qmgr_name}/channel/{channel_name}"
        return self._make_request(endpoint)
    
    def get_queue_attributes(self, qmgr_name: str, queue_name: str, format: str = "mqsc") -> Dict[str, Any]:
        if format.lower() == "mqsc":
            endpoint = f"{qmgr_name}/mqsc"
            attributes_payload = {
                'type': 'runCommandJSON',
                'name': queue_name,
                'command': 'DISPLAY',
                'qualifier': 'queue',
                'responseParameters': [
                    'ALL'
                ]
            }
            
            return self._make_mqsc_request(endpoint, attributes_payload)
        
        #return self._make_request(endpoint)


# Singleton instance
mq_client = MQClient()