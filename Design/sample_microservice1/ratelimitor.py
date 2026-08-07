# Rate limitor is implemented to avoid the unnecessary load on the server to avoid
# unnecessary burst of the traffic.

import asyncio
import time
from collections import deque
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Token bucket algorithm maintains the overall traffic rate but allows burst of traffic.
# easy to implement.
class RateLimitor(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.tokens = 5
        self.last_refill = time.monotonic()
        self.lock = asyncio.Lock()
        self.refresh_rate = 1  # tokens per second

    async def dispatch(self, request, call_next):

        async with self.lock:
            current_time = time.monotonic()
            self.tokens = min(5, self.tokens + (current_time - self.last_refill) * self.refresh_rate)
            self.last_refill = current_time

            if self.tokens < 1:
                return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

            self.tokens -= 1

        return await call_next(request)

# Ideally leaky bucket need to have the queue which holds the requests and then process at
# the constant rate, but it wastes cpu time and resources so, we are using lazy filling approach here.
# The lazy filling approach is very much similar to token bucket algorithm.

# laeakybucket algorithm maintains constant rate of traffic irrespective of burst of traffic
# but rejects the recent requests if the bucket is full. It is more complex to implement than token bucket algorithm.
class LeakyBucketRateLimiter(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.capacity = 5
        self.tokens = 0
        self.last_check = time.monotonic()
        self.lock = asyncio.Lock()
        self.leak_rate = 1 # tokens per second

    async def dispatch(self, request, call_next):
        async with self.lock:
            current_time = time.monotonic()
            elapsed_time = current_time - self.last_check
            self.tokens = max(0, self.tokens - elapsed_time * self.leak_rate)
            self.last_check = current_time

            if self.tokens >= self.capacity:
                return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

            self.tokens += 1

        return await call_next(request)

# maintains the overall traffic rate but allows burst of traffic in a fixed window of time.
# can cause double bursting if the requests are made at the end of one window and start of another window.
# easy to implement.
class Fixed_window_rate_limiter(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.capacity = 5
        self.token = 0
        self.window_start = time.monotonic()
        self.lock = asyncio.Lock()

    async def dispatch(self, request, call_next):

        async with self.lock:
            current_time = time.monotonic()

            if current_time - self.window_start >= 1:
                self.token = 0
                self.window_start = current_time

            if self.token >= self.capacity:
                return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

            self.token += 1
        return await call_next(request)

# avoids double bursting by maintaining the overall traffic rate but allows burst of traffic in a sliding window of time.
# needs cpu and memory resources to maintain the queue of requests time in the sliding window.
class sliding_window_rate_limiter(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.requests = deque()
        self.lock = asyncio.Lock()

    async def dispatch(self, request, call_next):
        async with self.lock:
            current_time = time.monotonic()

            while self.requests and current_time - self.requests[0] >= 10:
                self.requests.popleft()

            if len(self.requests) >= 5:
                return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

            self.requests.append(current_time)

        return await call_next(request)