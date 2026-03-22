import json
import uuid
from typing import List, Optional

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractExchange

from src.config import settings
from src.rabbitmq.tasks.CertificateSchema import AbstractCertificateSchema
from src.rabbitmq.tasks.HeadersSchema import HeadersSchema, CertificateTypes



class RabbitConnection:
    def __init__(self):
        self._connection: Optional[AbstractConnection] = None
        self._channel: Optional[AbstractChannel] = None
        self._exchange: Optional[AbstractExchange] = None
        self._active_consumers: dict = {}

    async def connect(self) -> None:
        """Подключение к RabbitMQ и инициализация обменника."""
        self._connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=int(settings.RABBITMQ_PORT),
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            ssl=settings.RABBITMQ_SSL,
            reconnect_interval=5,
        )
        self._channel = await self._connection.channel(publisher_confirms=False)
        self._exchange = await self._channel.declare_exchange(
            "default", durable=True
        )


    async def disconnect(self) -> None:
        """Корректное закрытие соединения."""
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    async def send_messages(
        self,
        messages: List[AbstractCertificateSchema],
        routing_key: str,
        headers: HeadersSchema,
        department: str,
    ) -> None:
        """Отправка сообщений без транзакций и повторных попыток."""
        if not self._connection or self._connection.is_closed:
            await self.connect()



        # Гарантируем существование очереди
        queue = await self._channel.declare_queue(name=routing_key, durable=True)
        await queue.bind(self._exchange, routing_key=routing_key)
        for msg in messages:
            body = json.dumps(msg.model_dump()).encode()

            await self._exchange.publish(
                aio_pika.Message(
                    body=body,
                    message_id=str(uuid.uuid4()),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    headers={"certificate_type": headers.certificate_type.value, "department": department}

                ),
                routing_key=routing_key
            )


class CertificateRabbitmqPublisher(RabbitConnection):
    async def send_order_messages(
            self,
            messages: List[AbstractCertificateSchema],
            certificate_type: CertificateTypes,
            department: str,
    ) -> None:
        await super().send_messages(messages=messages, routing_key='render_tasks', headers=HeadersSchema(certificate_type=certificate_type), department=department)
