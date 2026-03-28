from fastapi import FastAPI

from src.domain.client.router import router as client_router
from src.domain.vehicle.router import router as vehicle_router
from src.security.domain.user.router import router as auth_router
from src.core.exceptions import setup_exception_handlers

app = FastAPI()

# Inicializamos nossos validadores de exception customizados
setup_exception_handlers(app)

app.include_router(vehicle_router)
app.include_router(client_router)
app.include_router(auth_router)
