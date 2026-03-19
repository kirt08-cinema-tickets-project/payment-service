import grpc

from src.core.grpc.exceptions import ServiceException


class PaymentNotFoundException(ServiceException):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message: str = "Payment not found"


class MultiplePaymentsFoundException(ServiceException):
    grpc_status = grpc.StatusCode.FAILED_PRECONDITION
    message: str = "Multiple Payments exist"


class NotPaymentMethodFoundException(ServiceException):
    grpc_status = grpc.StatusCode.NOT_FOUND
    message: str = "Saved payment method not found"