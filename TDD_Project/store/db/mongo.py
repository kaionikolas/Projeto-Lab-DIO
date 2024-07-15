from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings


class MongoClient:
    def__init__(self) -> None:
        self.client: AsyncIOMotorClient =  AsyncIOMotorClient(settings.DATABASE_URL)

    def get() ->  AsyncIOMotorClient:
        return self.client

db_client = MongoClient()
