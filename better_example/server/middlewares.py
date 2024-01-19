from log.custom_logger import logger
import uuid
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class RequestIdInjectionMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    # Add request ID for logging to context
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request_id = str(uuid.uuid4().hex)
        with logger.contextualize(request_id=request_id):
            try:
                return await self.app(scope, receive, send)

            except Exception as ex:
                logger.error(f"Request failed: {ex}")
                return JSONResponse(content={"success": False}, status_code=500)
