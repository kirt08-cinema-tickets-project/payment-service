from src.core.config import settings
from src.core.clients.booking import BookingClient

booking_url = settings.grpc.booking_client.host + ":" + settings.grpc.booking_client.port
booking_client = BookingClient(host = booking_url)