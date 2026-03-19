import grpc
import logging

from functools import wraps

log = logging.getLogger(__name__)


class ServiceException(Exception):
    grpc_status = grpc.StatusCode.INTERNAL
    message: str = ""

def grpc_exception_handler_class(cls):
    for attr_name in dir(cls):
        if attr_name.startswith("_"):
            continue

        attr = getattr(cls, attr_name)
        if callable(attr) and hasattr(attr, "__code__") and attr.__code__.co_flags & 0x80:
            
            def make_wrapper(func):
                @wraps(func)
                async def wrapper(self, request, context):
                    try:
                        return await func(self, request, context)
                    except ServiceException as e:
                        log.error(
                            f"{type(e).__name__}: {e.message}"
                        )
                        await context.abort(e.grpc_status, e.message)
                return wrapper
            setattr(cls, attr_name, make_wrapper(attr))
    return cls