from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional, Any
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from models.events import Event
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: str
    DB_NAME: str
    SECRET_KEY: Optional[str] = None

    @classmethod
    async def initialize_database(cls):
        # create instance to access env vars
        settings = cls()
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        db = client[settings.DB_NAME]

        await init_beanie(
            database=db,
            document_models=[Event, User],
        )

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

        # des_body = body.model_dump()
        # des_body = {k: v for k, v in des_body.items() if v is not None}
        # update_query = {"$set": {field: value for field, value in des_body.items()}}
        # doc = await self.get(doc_id)

        # if not doc:
        #     return False
        # await doc.update(update_query)
        # return doc

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.model_dump()
        des_body = {key: value for key, value in des_body.items() if value is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
