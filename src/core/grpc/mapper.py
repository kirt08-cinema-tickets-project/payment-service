from kirt08_contracts.payment import payment_pb2

from src.payment.schemas import (
    CreatePaymentRequestDTO,
    SeatType,
    ProcessPaymentEventRequestDTO,
    PaymentMethodDatabase,
    PaymentMethodItem,
)

class PaymentMapper:
    @classmethod
    def grpc_creation_to_dto(cls, data: payment_pb2.CreatePaymentRequest) -> CreatePaymentRequestDTO:
        return CreatePaymentRequestDTO(
            user_id = data.user_id,
            screening_id = data.screening_id,
            seats = [
                SeatType(
                    seat_id = temp.seat_id,
                    price = temp.price
                )
                for temp in data.seats
            ],
            payment_method_id = data.payment_method_id,
            save_payment_method = data.save_payment_method
        )
    
    @classmethod
    def grpc_event_to_dto(cls, proto_message: payment_pb2.ProcessPaymentEventRequest) -> ProcessPaymentEventRequestDTO:
        return ProcessPaymentEventRequestDTO(
            event = proto_message.event,
            payment_id = proto_message.payment_id,
            booking_id = proto_message.booking_id,
            user_id = proto_message.user_id,
            save_payment_method = proto_message.save_payment_method,
            provider_method_id = proto_message.provider_method_id or None,
            card_first6 = proto_message.card_first6 or None,
            card_last4 = proto_message.card_last4 or None,
            bank = proto_message.bank or None,
            brand = proto_message.brand or None
        )
    
    @classmethod
    def get_payment_methods_dto_to_grpc(cls, data: list[PaymentMethodDatabase]) -> payment_pb2.GetUserPaymentMethodsResponse:
        if not data:
            return []
        
        return [
            payment_pb2.PaymentMethodItem(
                id = str(temp.id),
                bank = temp.bank,
                brand = temp.brand,
                first6 = temp.first6,
                last4 = temp.last4
            )
            for temp in data
        ] 