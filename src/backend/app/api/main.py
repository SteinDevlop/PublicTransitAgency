from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.middlewares import add_middlewares
from backend.app.api.routes import (
    card_cud_service,
    card_query_service,
    incidence_CUD_service,
    #incidence_query_service,
    #maintainance_status_cud_service,
    maintainance_status_query_service,
    maintance_cud_service,
    maintance_query_service,
    #payment_cud_service,
    #payment_query_service,
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
    #type_card_cud_service,
    type_card_query_service,
    #transport_unit_cud_service,
    #transport_unit_query_service,
    user_CUD_service,
    user_query_service,
    type_movement_cud_service,
    type_movement_query_service,
    type_transport_cud_service,
    type_transport_query_service,
    rol_user_cud_service,
    rol_user_query_service,
    price_cud_service,
    #price_query_service,
    movement_cud_service,
    movement_query_service
)

api_router = FastAPI(title=settings.PROJECT_NAME)

# Middlewares Globales
add_middlewares(api_router)

# CORS Middleware
api_router.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the routes for different services.
api_router.include_router(card_cud_service.app)
api_router.include_router(card_query_service.app)
api_router.include_router(maintance_cud_service.app)
api_router.include_router(maintance_query_service.app)
#api_router.include_router(type_card_cud_service.app) backend.app. for everyone
api_router.include_router(type_card_query_service.app)
api_router.include_router(user_CUD_service.app)
#api_router.include_router(user_query_service.app)
api_router.include_router(type_movement_cud_service.app)
#api_router.include_router(type_movement_query_service.app)
api_router.include_router(type_transport_cud_service.app)
#api_router.include_router(type_transport_query_service.app)
api_router.include_router(rol_user_cud_service.app)
#api_router.include_router(rol_user_query_service.app)
api_router.include_router(price_cud_service.app)
#api_router.include_router(price_query_service.app)
api_router.include_router(movement_cud_service.app)
#api_router.include_router(movement_query_service.app)
#api_router.include_router(payment_cud_service.app)
#api_router.include_router(payment_query_service.app)
#api_router.include_router(maintainance_status_cud_service.app)
api_router.include_router(maintainance_status_query_service.app)
#api_router.include_router(transport_unit_cud_service.app)
#api_router.include_router(transport_unit_query_service.app)
#api_router.include_router(schedule_cud_service.app)
#api_router.include_router(schedule_query_service.app)
api_router.include_router(incidence_CUD_service.app)
#api_router.include_router(incidence_query_service.app)
#api_router.include_router(ticket_cud_service.app)
#api_router.include_router(ticket_query_service.app)
##api_router.include_router(routes_cud_service.app)
#api_router.include_router(shifts_cud_service.app)
#api_router.include_router(shifts_query_service.app)
#api_router.include_router(stops_cud_service.app)
#api_router.include_router(stops_query_service.app)

