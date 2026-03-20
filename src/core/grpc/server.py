import grpc
import logging

from aioyookassa import YooKassa

from kirt08_contracts.payment import payment_pb2_grpc
from kirt08_contracts.refund import refund_pb2_grpc

from src.core.config import settings
from src.core.grpc.payments import gRPC_Payments_Server
from src.core.grpc.refund import gRPC_Refund_Server


log = logging.getLogger(__name__)


async def serve(yookassa_client: YooKassa):
    log.info("Server starting up...")

    server = grpc.aio.server()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        servicer = gRPC_Payments_Server(
            yookassa_client = yookassa_client
        ),
        server = server 
    )

    refund_pb2_grpc.add_RefundServiceServicer_to_server(
        servicer = gRPC_Refund_Server(
            yookassa_client = yookassa_client
        ),
        server = server
    )

    server.add_insecure_port(f"{settings.grpc.server.host}:{settings.grpc.server.port}")
    await server.start()
    log.info("Server successfully started!")
    
    await server.wait_for_termination()
