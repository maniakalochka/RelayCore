from typing import Any

from fastapi import Request


def get_rabbitmq(request: Request) -> Any:
    return request.app.state.rabbit
