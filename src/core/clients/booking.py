import grpc
from typing import TYPE_CHECKING

from kirt08_contracts.booking import booking_pb2, booking_pb2_grpc

from src.core.clients.mapper import BookingMapper

from src.shared.schemas import CreateReservationResponse

if TYPE_CHECKING:
    from src.payment.schemas import SeatType


class BookingClient:
    def __init__(self, host):
        self._channel = grpc.aio.insecure_channel(host)
        self._stub = booking_pb2_grpc.BookingServiceStub(self._channel)

    async def CreateReservation(self, user_id: str, screening_id: str, seats: list["SeatType"]) -> CreateReservationResponse:
        request = BookingMapper.form_create_request(
            user_id = user_id,
            screening_id = screening_id,
            seats = seats 
        )
        grpc_response = await self._stub.CreateReservation(request)
        
        response = BookingMapper.creation_grpc_to_dto(request = grpc_response)
        return response
    

    async def ConfirmBooking(self, booking_id: str, user_id: str) -> bool:
        request = booking_pb2.ConfirmBookingRequest(
            booking_id = booking_id,
            user_id = user_id
        )
        grpc_response = await self._stub.ConfirmBooking(request)
        return grpc_response.ok
    

    async def CancelBooking(self, booking_id: str, user_id: str) -> bool:
        request = booking_pb2.CancelBookingRequest(
            booking_id = booking_id,
            user_id = user_id
        )
        grpc_response = await self._stub.CancelBooking(request)
        return grpc_response.ok
        