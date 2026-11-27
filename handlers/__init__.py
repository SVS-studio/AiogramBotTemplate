from aiogram import Router

from . import common, echo


def setup_routers() -> Router:
    """Build and return the root router for the application."""
    router = Router(name="root")
    router.include_routers(common.router, echo.router)
    return router
