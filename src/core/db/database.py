from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings


class DataBase:
    def __init__(self, url: URL, echo: bool = False):
        self._url = url
        self._echo = echo

        self._engine = None
        self._sessionmaker = None


    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_async_engine(
                url = self._url,
                echo = self._echo
            )
        return self._engine
    
    @property
    def sessionmaker(self):
        if self._sessionmaker is None:
            self._sessionmaker = async_sessionmaker(
                bind = self.engine,
                expire_on_commit = False
            )
        return self._sessionmaker
        

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self.sessionmaker() as session:
            yield session


db = DataBase(
    url = settings.db.async_url,
    echo = settings.db.echo
)