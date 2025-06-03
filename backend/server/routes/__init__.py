from .auth import router as auth_router
from .devices import router as device_router
from .events import router as event_router
from .users import router as user_router
from .upload import router as upload_router
__all__ = ["auth_router","user_router","device_router", "event_router", "upload_router"]
