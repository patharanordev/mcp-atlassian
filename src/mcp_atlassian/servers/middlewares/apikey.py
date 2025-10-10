from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

class ApiKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, x_api_key_header: str = "x-api-key", scheme: str = "Bearer"):
        super().__init__(app)
        self.x_api_key = x_api_key_header.lower()
        self.scheme = scheme

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = request.headers.get(self.x_api_key)
        if token:
            hdrs = list(request.scope["headers"])
            hdrs.append((b"authorization", f"{self.scheme} {token}".encode()))
            request.scope["headers"] = hdrs
        return await call_next(request)