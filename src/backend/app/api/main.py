from fastapi import APIRouter,FastAPI

from backend.app.api.routes import (
    #assign_rol_user_service,
    #assign_type_movement_service,
    #assign_type_transport_service,
    #assing_price_service,
    card_cud_service,
    card_query_service,
    #incidence_CUD_service,
    #incidence_query_service,
    #maintainance_status_CUD_service,
    maintance_cud_service,
    maintance_query_service,
    #mantainance_status_query_service,
    #movement_service,
    #payment_CUD_service,
    #payment_service_recharge,
    #routes_CUD_service,
    #routes_query_service,
    #schedule_CUD_service,
    #schedule_query_service,
    #shifts_CUD_service,
    #stops_CUD_service,
    #stops_query_service,
    #shifts_query_service,
    #user_service,
    #ticket_CUD_service,
    #ticket_query_service,
    type_card_cud_service,
    type_card_query_service,
    #transport_unit_CUD_service,
    #transport_unit_query_service
)

api_router = APIRouter()
api_router.include_router(card_cud_service.app)
api_router.include_router(card_query_service.app)
api_router.include_router(maintance_cud_service.app)
api_router.include_router(maintance_query_service.app)
api_router.include_router(type_card_cud_service.app)
api_router.include_router(type_card_query_service.app)

app = FastAPI()

app.include_router(api_router)