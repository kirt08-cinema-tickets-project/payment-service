from pydantic import BaseModel


class BaseGRPC(BaseModel):
    host: str = ""
    port: str = ""

class ServerConfig(BaseGRPC):
    ...

class GrpcConfig(BaseModel):
    server: ServerConfig = ServerConfig()