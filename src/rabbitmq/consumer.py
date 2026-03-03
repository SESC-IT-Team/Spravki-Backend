import asyncio
import logging
import json
import aio_pika
from aio_pika import ExchangeType
from src.config import Settings
from src.rabbitmq.tasks.HeadersSchema import HeadersSchema, CertificateTypes
from src.rabbitmq.tasks.impl.SocialFoundationCertificate import SocialFoundationCertificate
from src.rabbitmq.tasks.impl.SocialFoundationCertificateSchema import SocialFoundationCertificateSchema
from src.config import settings
from src.services.order_service import OrderService

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info('Connecting to RabbitMQ...')

    try:
        connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=int(settings.RABBITMQ_PORT),
            ssl=settings.RABBITMQ_SSL,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
        )


        channel = await connection.channel()
        queue = await channel.declare_queue("render_tasks", durable=True)


        async def on_message(message):
            logger.info(f"Получено сообщение: {message.body.decode()}")
            logger.info(f"{type(message)}")

            raw_type = message.headers.get("certificate_type")
            certificate_type = CertificateTypes(raw_type)
            if certificate_type == CertificateTypes.SocialFoundation:
                body = SocialFoundationCertificateSchema.model_validate(json.loads(message.body.decode()))
                await OrderService().create_order(certificate_type=certificate_type, full_name=body.fio)
                SocialFoundationCertificate.render(body)

            await message.ack()

        await channel.set_qos(prefetch_count=1)
        await queue.consume(on_message)

        logger.info("Consumer запущен. Для остановки нажмите Ctrl+C...")
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info("\nЗавершение работы consumer'а...")
    finally:
        if 'connection' in locals():
            await connection.close()


if __name__ == "__main__":
    asyncio.run(main())