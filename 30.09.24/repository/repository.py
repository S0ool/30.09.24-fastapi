from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from database import async_session_maker


class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls, filters: dict = None, join_related: list = None):
        async with async_session_maker() as session:
            query = select(cls.model)

            if join_related:
                for relation in join_related:
                    query = query.options(joinedload(relation))

            if filters:
                for field, value in filters.items():
                    query = query.filter(getattr(cls.model, field) == value)

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, model_id, filters: dict = None, join_related: list = None):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)

            if join_related:
                for relation in join_related:
                    query = query.options(joinedload(relation))

            if filters:
                for field, value in filters.items():
                    query = query.filter(getattr(cls.model, field) == value)

            result = await session.execute(query)
            model = result.scalar_one_or_none()
            if model is None:
                raise HTTPException(status_code=404, detail='not found')

            return model

    @classmethod
    async def create(cls, data):
        async with async_session_maker() as session:
            model = cls.model(**data.dict())
            session.add(model)
            await session.commit()

            return model

    @classmethod
    async def update(cls, model_id, data: dict):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            model = result.scalar_one_or_none()
            if model is None:
                raise HTTPException(status_code=404, detail='not found')

            for key, value in data.items():
                if hasattr(model, key):
                    setattr(model, key, value)

            session.add(model)
            await session.commit()

            return model

    @classmethod
    async def delete(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            model = result.scalar_one_or_none()
            if model is None:
                raise HTTPException(status_code=404, detail='not found')

            await session.delete(model)
            await session.commit()

            return 'deleted'
