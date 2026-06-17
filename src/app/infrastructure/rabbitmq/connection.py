import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection


class RabbitMQ:
    def __init__(
        self,
        url: str,
        connection: AbstractRobustConnection | None = None,
        channel: aio_pika.abc.AbstractChannel | None = None,
    ):
        self.url = url
        self.connection = connection
        self._channel = channel

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.url)
        self._channel = await self.connection.channel()

        await self.channel.declare_queue("node_health_check", durable=True)

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()

    @property
    def channel(self) -> AbstractChannel:
        if self._channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")
        return self._channel
