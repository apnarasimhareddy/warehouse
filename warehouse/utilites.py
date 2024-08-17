from abc import ABC, abstractmethod
import httpx
from warehouse.core.config import settings


class APIClient(ABC):
    
    @abstractmethod
    async def get_data(self, endpoint: str, params: dict = None, query:dict=None) -> dict:
        pass

    
class BerryDevAPI(APIClient):
    def __init__(self):
        self.api_key = settings.api_key
        self.base_url = "https://challenge.berrydev.ai/api"

    async def get_data(self, endpoint: str, params: dict = None, query:dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response:httpx.Response = await client.get(f"{self.base_url}/{endpoint}", query= query, params=params, headers={"X-API-Key": f"{self.api_key}"})
            response.raise_for_status()
            return response.json()


class Client:
    @staticmethod
    def get_client(api_type: str, **kwargs) -> APIClient:
        if api_type == "berrydev":
            return BerryDevAPI()
        else:
            raise ValueError(f"Unknown API type: {api_type}")
        
