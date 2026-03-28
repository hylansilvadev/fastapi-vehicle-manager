from fastapi import FastAPI

from src.controller.vehicle_controller import router as vehicle_router
from src.core.exceptions import setup_exception_handlers

app = FastAPI()

# Inicializamos nossos validadores de exception customizados
setup_exception_handlers(app)

app.include_router(vehicle_router)
