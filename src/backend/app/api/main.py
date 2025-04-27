from fastapi import APIRouter, FastAPI

from backend.app.api.routes import (

    card_cud_service,
    card_query_service,
    #incidence_CUD_service,
    #incidence_query_service,
    #maintainance_status_CUD_service,
    maintance_cud_service,
    maintance_query_service,
    #mantainance_status_query_service,
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
    #transport_unit_query_service,
    #user_cud_service,
    #user_query_service,
    #type_movement_cud_service,
    #type_movement_query_service,
    #type_transport_cud_service,
    #type_transport_query_service,
    #rol_user_cud_service,
    #rol_user_query_service,
    #price_cud_service,
    #price_query_service,
    #movement_cud_service,
    #movement_query_service
)

# Include the API routes.
api_router = APIRouter()

# Include the routes for different services.
api_router.include_router(card_cud_service.app)
api_router.include_router(card_query_service.app)
api_router.include_router(maintance_cud_service.app)
api_router.include_router(maintance_query_service.app)
api_router.include_router(type_card_cud_service.app)
api_router.include_router(type_card_query_service.app)

# Initialize the FastAPI application.
app = FastAPI()

# Include the router for the API.
app.include_router(api_router)
