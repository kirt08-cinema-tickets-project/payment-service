from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class DatabaseConfig(BaseModel):
    username : str = ""
    password : SecretStr = ""
    host : str = ""
    port : str = ""
    name : str = ""

    echo : bool = True

    @property
    def async_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.username,
            password=self.password.get_secret_value(),
            host = self.host,
            port=self.port,
            database=self.name
        )