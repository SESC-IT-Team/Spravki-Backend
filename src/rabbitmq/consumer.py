import asyncio
import logging

import aio_pika

from src.config import Settings
from src.rabbitmq.tasks.HeadersSchema import HeadersSchema, CertificateTypes
from src.rabbitmq.tasks.impl.SocialFoundationCertificate import SocialFoundationCertificate
from src.rabbitmq.tasks.impl.SocialFoundationCertificateSchema import SocialFoundationCertificateSchema

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
            host=Settings.RABBITMQ_HOST,
            port=int(Settings.RABBITMQ_PORT),
            ssl=Settings.RABBITMQ_SSL,
            login=Settings.RABBITMQ_USER,
            password=Settings.RABBITMQ_PASSWORD,
        )

        channel = await connection.channel()
        queue = await channel.declare_queue("render_tasks", durable=True)

        async def on_message(message):
            logger.info(f"Получено сообщение: {message.body.decode()}")
            logger.info(f"{type(message)}")

            headers = HeadersSchema.model_validate(message.headers)

            if headers.certificate_type == CertificateTypes.SocialFoundation:
                body = SocialFoundationCertificateSchema.model_validate(message.body.decode())
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