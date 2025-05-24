from .devices import router as device_router
from .events import router as event_router
from .users import router as user_router

__all__ = ["user_router","device_router", "event_router"]
