from aiogram import Router
from .start import router as start_router
from .stop import router as stop_router
from .messages import router as messages_router
from .callbacks import router as callbacks_router

router = Router()
router.include_router(start_router)
router.include_router(stop_router)
router.include_router(messages_router)
router.include_router(callbacks_router)
