from aioyookassa import YooKassa

from kirt08_contracts.payment import payment_pb2_grpc, payment_pb2

from src.core.db import db
from src.core.grpc.mapper import PaymentMapper
from src.core.grpc.exceptions import grpc_exception_handler_class

from src.payment import PaymentHandler


@grpc_exception_handler_class
class gRPC_Payments_Server(payment_pb2_grpc.PaymentServiceServicer):
    def __init__(self, yookassa_client: YooKassa):
        self._payment_handler = PaymentHandler(
            db = db,
            yookassa_client = yookassa_client
        )

    async def CreatePayment(self, request, context):
        data_dto = PaymentMapper.grpc_creation_to_dto(data = request)
        url = await self._payment_handler.CreatePayment(data = data_dto)
        response = payment_pb2.CreatePaymentResponse(url = url)
        return response
    
    async def ProcessPaymentEvent(self, request, context):
        data_dto = PaymentMapper.grpc_event_to_dto(proto_message = request)
        res = await self._payment_handler.ProcessPaymentEvent(data = data_dto)
        response = payment_pb2.ProcessPaymentEventResponse(
            ok = res
        )
        return response

    async def GetUserPaymentMethods(self, request, context):
        user_id = request.user_id
        res = await self._payment_handler.GetUserPaymentMethods(user_id = user_id)
        response = payment_pb2.GetUserPaymentMethodsResponse(
            methods = PaymentMapper.get_payment_methods_dto_to_grpc(data = res)
        )
        return response
    
    async def DeleteUserPaymentMethod(self, request, context):
        user_id, method_id = request.user_id, request.method_id
        res = await self._payment_handler.DeleteUserPaymentMethod(
            user_id = user_id,
            method_id = method_id
        )
        response = payment_pb2.DeleteUserPaymentMethodResponse(ok = res)
        return response