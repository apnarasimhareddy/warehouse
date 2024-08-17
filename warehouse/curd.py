from sqlalchemy import select,insert
from sqlalchemy.ext.asyncio import AsyncSession
from warehouse.models import Customers,Campaigns
from warehouse.schemas import CustomerSchema,CampaignsSchema
from abc import ABC, abstractmethod

class SyncTragetDB(ABC):

    def __init__(self,db:AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def synchronize_data(self,db:AsyncSession,data:list[dict])->list[dict]:
        pass

    @abstractmethod
    async def fetch_all(db:AsyncSession,offset:int,limit:int)->list[CustomerSchema] | list[CampaignsSchema]:
        pass

    @abstractmethod
    async def get_status_by(db:AsyncSession,status:str)->list[CustomerSchema] | list[CampaignsSchema]:
        pass


class CustomersDB(SyncTragetDB):
    async def synchronize_data(self,data:list[dict])->list[dict]:
        return (await self.db.scalar(insert(Customers),data)) 
    
    async def fetch_all(self,offset:int,limit:int)->list[CustomerSchema]:
        query = select(Customers).offset(offset).limit(int)
        result = await self.db.execute(query)
        result = result.scalars().all()
        return result

    async def get_status_by(self,status:str)->list[CustomerSchema]:
        query = select(Customers).where(Customers.status==status)
        result = await self.db.execute(query)
        result = result.scalars().all()
        return result
    
class CampaignsDB(SyncTragetDB):
    async def synchronize_data(self,data:list[dict])->list[dict]:
        return (await self.db.scalar(insert(Campaigns),data)) 
    
    async def fetch_all(self,offset:int,limit:int)->list[CampaignsSchema]:
        query = select(Campaigns).offset(offset).limit(int)
        result = await self.db.execute(query)
        result = result.scalars().all()
        return result

    async def get_status_by(self,status:str)->list[CampaignsSchema]:
        query = select(Campaigns).where(Customers.status==status)
        result = await self.db.execute(query)
        result = result.scalars().all()
        return result

class AsyncDB:
    
    @staticmethod
    async def targetDB(source:str,db:AsyncSession):
        if source == 'customers':
            return CustomersDB(db)
        elif source == 'campaigns':
            return CampaignsDB(db)
        else:
            raise ValueError(f"Unknown source: {source}")