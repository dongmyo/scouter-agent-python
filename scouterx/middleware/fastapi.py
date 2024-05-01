from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from scouterx.strace.tracemain import start_http_service, end_http_service


class FastapiMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        ctx = request.scope
        new_ctx, _ = start_http_service(ctx, request)

        try:
            response = await call_next(request)
        finally:
            end_http_service(new_ctx, request, response)

        return response
