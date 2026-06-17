import uuid

import aio_pika
from aio_pika.abc import AbstractChannel

from app.broker.constants import NODE_HEALTH_CHECK_QUEUE


class NodePublisher:
    def __init__(self, channel: AbstractChannel):
        self.channel = channel

    async def publish_health_check(self, node_id: uuid.UUID) -> None:
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=str(node_id).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=NODE_HEALTH_CHECK_QUEUE,
        )
