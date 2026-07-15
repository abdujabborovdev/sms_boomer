from aiogram import Router

from .help import router as help_router
from .start import router as start_router
from .sms import router as sms_router
from .tolov import router as tolov_router
from .admin import router as admin_router
router = Router()

router.include_router(start_router)
router.include_router(help_router)
router.include_router(sms_router)
router.include_router(tolov_router)
router.include_router(admin_router)