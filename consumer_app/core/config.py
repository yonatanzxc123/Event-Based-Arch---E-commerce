import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "orders.events")
EXCHANGE_TYPE = "fanout"
QUEUE_NAME = os.getenv("QUEUE_NAME", "order-service-queue")
