from aioyookassa import YooKassa

from kirt08_contracts.refund import refund_pb2, refund_pb2_grpc

from src.core.db import db
from src.core.grpc.exceptions import grpc_exception_handler_class

from src.refund import RefundHandler


@grpc_exception_handler_class
class gRPC_Refund_Server(refund_pb2_grpc.RefundServiceServicer):
    def __init__(self, yookassa_client: YooKassa):
        self._refund_handler = RefundHandler(
            db = db,
            yookassa_client = yookassa_client
        )

    async def CreateRefund(self, request, context):
        res = await self._refund_handler.CreateRefundRequest(
            booking_id = request.booking_id,
            user_id = request.user_id
        )
        response = refund_pb2.CreateRefundResponse(
            ok = res
        )
        return response


    async def ProcessRefundEvent(self, request, context):
        res = await self._refund_handler.ProcessRefundEvent(
            event = request.event,
            provider_refund_id = request.provider_refund_id,
            status = request.status
        )
        response = refund_pb2.ProcessRefundEventResponse(
            ok = res
        )
        return response