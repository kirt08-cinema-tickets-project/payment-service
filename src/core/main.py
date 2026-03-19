import logging
import asyncio

from aioyookassa import YooKassa

from src.core.config.settings import settings

from src.core.grpc.server import serve


logging.basicConfig(
    format=settings.logger.format, 
    level=settings.logger.log_level   
)


async def main():
    yookassa_client = YooKassa(
        api_key = settings.yookassa.secret_key.get_secret_value(),
        shop_id = settings.yookassa.shop_id
    )    
    await serve(yookassa_client)


if __name__ == "__main__":
    asyncio.run(main())