from typing import TYPE_CHECKING
from kirt08_contracts.booking import booking_pb2

from src.shared.schemas import CreateReservationResponse

if TYPE_CHECKING:
    from src.payment.schemas import SeatType


class BookingMapper:
    @classmethod
    def form_create_request(cls, user_id: str, screening_id: str, seats: list["SeatType"]) -> booking_pb2.CreateReservationRequest:
        return booking_pb2.CreateReservationRequest(
            user_id = user_id,
            screening_id = screening_id,
            seats = [
                booking_pb2.SeatInput(
                    seat_id = seat.seat_id,
                    price = seat.price
                )
                for seat in seats
            ]
        ) 
    
    @classmethod
    def creation_grpc_to_dto(cls, request: booking_pb2.CreateReservationResponse) -> CreateReservationResponse:
        return CreateReservationResponse(
            order_id = request.order_id,
            tickets_id = request.tickets_id,
            amount = request.amount 
        )