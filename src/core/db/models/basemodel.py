import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at : Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    updated_at : Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    