import asyncio
import uuid

from aio_pika.abc import AbstractIncomingMessage

from app.broker.constants import NODE_HEALTH_CHECK_QUEUE
from app.core.config import settings
from app.core.logging import get_logger
from app.infrastructure.rabbitmq.connection import RabbitMQ
from app.main import app

logger = get_logger(__name__)


async def process(msg: AbstractIncomingMessage) -> None:
    async with msg.process():
        node_id = uuid.UUID(msg.body.decode())
        logger.info(f"Processing health check for node: {node_id}")


async def main() -> None:
    rabbit = RabbitMQ(settings.RABBITMQ_URL)
    await rabbit.connect()

    app.state.rabbit = rabbit

    queue = await rabbit.channel.declare_queue(NODE_HEALTH_CHECK_QUEUE, durable=True)

    await queue.consume(process)
    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
