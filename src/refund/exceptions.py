import grpc

from src.core.grpc.exceptions import ServiceException


class RefundNotFoundException(ServiceException):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message = "Refund was not found"