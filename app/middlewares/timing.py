import time
from starlette.requests import Request
from starlette.responses import Response

async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response: Response = await call_next(request)
    dur_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{dur_ms:.2f}"
    # Bu yerda logger ishlatib yozib qo'yishingiz mumkin
    return response
