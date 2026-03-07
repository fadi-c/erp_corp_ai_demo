from ninja import NinjaAPI
from .endpoints import router as endpoints_router

api = NinjaAPI()

api.add_router("", endpoints_router)