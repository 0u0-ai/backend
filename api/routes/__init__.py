from fastapi import APIRouter

from .refresh import router as refresh_router
from .chat import router as chat
from .base import router as base

router = APIRouter()

router.include_router(refresh_router)
router.include_router(chat)
router.include_router(base)
