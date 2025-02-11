from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from fastapi import Depends

from ..tables import Object, StateObject, User, ObjectToUser
from ..database import get_session


class ObjectRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def count_row(self) -> int:
        response = select(func.count(Object.id))
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def get_limit_object(self, start: int, end: int) -> list[Object]:
        response = select(Object).where(Object.is_deleted == False).offset(start).fetch(end).order_by(Object.id)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def get_all_object(self) -> list[Object]:
        response = select(Object).where(Object.is_deleted == False).order_by(Object.id)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def get_all_state_object(self) -> list[StateObject]:
        response = select(StateObject)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def add(self, object: Object):
        try:
            self.__session.add(object)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def get_by_uuid(self, uuid: str) -> Object | None:
        response = select(Object).where(Object.uuid == uuid)
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def update(self, entity: Object):
        try:
            self.__session.add(entity)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def get_user_by_uuid_object(self, uuid: str) -> list[User]:
        entity = await self.get_by_uuid(uuid)
        response = select(User).join(ObjectToUser).where(ObjectToUser.id_object == entity.id)
        result = await self.__session.execute(response)
        return result.scalars().all()

    async def unique_object_to_user(self, uuid_object: str, uuid_user) -> bool:
        response = select(ObjectToUser).\
            join(Object).\
            join(User).\
            where(Object.uuid == uuid_object).\
            where(User.uuid == uuid_user)
        result = await self.__session.execute(response)
        entity = result.scalars().first()
        if entity is None:
            return True
        return False

    async def add_user_to_object(self, obj: Object, user: User):
        try:
            self.__session.add(ObjectToUser(
                id_object=obj.id,
                id_user=user.id
            ))
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def delete_user_to_object(self, uuid_object: str, uuid_user: str):
        response = select(ObjectToUser). \
            join(Object). \
            join(User). \
            where(Object.uuid == uuid_object). \
            where(User.uuid == uuid_user)
        result = await self.__session.execute(response)
        entity = result.scalars().first()
        if entity is None:
            raise Exception
        try:
            await self.__session.delete(entity)
            await self.__session.commit()
        except Exception:
            await self.__session.rollback()