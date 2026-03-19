from pydantic import BaseModel, SecretStr


class YookassaConfig(BaseModel):
    shop_id: str = ""
    secret_key: SecretStr = ""