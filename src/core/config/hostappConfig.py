from pydantic import BaseModel


class HostAppConfig(BaseModel):
    url: str = ""