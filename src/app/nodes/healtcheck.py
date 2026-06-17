"""
Minimal health check implementation for nodes. May open the TCP connecion.
"""

import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeHealthCheckResult:
    is_active: bool
    latency_ms: int | None
    error: str | None = None


class NodeHealthCheckService:
    def __init__(self, timeout_seconds: float = 3.0):
        self.timeout_seconds = timeout_seconds

    async def check_tcp(self, host: str, port: int) -> NodeHealthCheckResult:
        started_at = asyncio.get_running_loop().time()
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=self.timeout_seconds
            )
            writer.close()
            await writer.wait_closed()

            finished_at = asyncio.get_running_loop().time()
            latency_ms = int((finished_at - started_at) * 1000)

            return NodeHealthCheckResult(
                is_active=True,
                latency_ms=latency_ms,
            )
        except TimeoutError:
            return NodeHealthCheckResult(
                is_active=False,
                latency_ms=None,
                error=f"Connection timed out after {self.timeout_seconds} seconds",
            )

        except OSError as e:
            return NodeHealthCheckResult(
                is_active=False,
                latency_ms=None,
                error=f"OS error: {e}",
            )
