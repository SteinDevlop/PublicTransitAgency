from fastapi import APIRouter, FastAPI

from backend.app.api.routes import (

    card_cud_service,
    card_query_service,
    #incidence_cud_service,
    #incidence_query_service,
    maintainance_status_cud_service,
    maintance_cud_service,
    maintance_query_service,
    mantainance_status_query_service,
    #payment_cud_service,
    #payment_service_recharge,
    #routes_cud_service,
    #routes_query_service,
    #schedule_cud_service,
    #schedule_query_service,
    #shifts_cud_service,
    #stops_cud_service,
    #stops_query_service,
    #shifts_query_service,
    #user_service,
    #ticket_cud_service,
    #ticket_query_service,
    type_card_cud_service,
    type_card_query_service,
    #transport_unit_cud_service,
    #transport_unit_query_service,
    user_cud_service,
    user_query_service,
    type_movement_cud_service,
    type_movement_query_service,
    type_transport_cud_service,
    type_transport_query_service,
    rol_user_cud_service,
    rol_user_query_service,
    price_cud_service,
    price_query_service,
    movement_cud_service,
    movement_query_service
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

api_router.include_router(user_cud_service.app)
api_router.include_router(user_query_service.app)
api_router.include_router(type_movement_cud_service.app)
api_router.include_router(type_movement_query_service.app)
api_router.include_router(type_transport_cud_service.app)
api_router.include_router(type_transport_query_service.app)
api_router.include_router(rol_user_cud_service.app)
api_router.include_router(rol_user_query_service.app)
api_router.include_router(price_cud_service.app)
api_router.include_router(price_query_service.app)
api_router.include_router(movement_cud_service.app)
api_router.include_router(movement_query_service.app)

# Initialize the FastAPI application.
app = FastAPI()

# Include the router for the API.
app.include_router(api_router)
