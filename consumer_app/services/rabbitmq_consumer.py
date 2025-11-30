import json
import threading
from typing import Any

import pika
from pika import URLParameters

from consumer_app.core.config import (
    RABBITMQ_URL,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
    QUEUE_NAME,
)
from consumer_app.models.order import Order
from consumer_app.models.stored_order import StoredOrder
from consumer_app.services.order_store import order_store


def _process_message(body: bytes) -> None:
    data: Any = json.loads(body.decode("utf-8"))

    # Requirement: only handle orders with status == "new"
    if data.get("status") != "new":
        return

    order = Order(**data)

    # Requirement: shippingCost = 2% of totalAmount
    shipping_cost = round(order.totalAmount * 0.02, 2)

    stored = StoredOrder(order=order, shippingCost=shipping_cost)
    order_store.save(stored)


def start_consumer() -> None:
    params = URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Same exchange as producer
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        durable=True,
    )

    # Declaring a durable queue for this service
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Bind queue to the fanout exchange
    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME)

    def on_message(ch, method, properties, body: bytes):
        try:
            _process_message(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            # avoid infinite redelivery loops
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=on_message,
        auto_ack=False,
    )

    channel.start_consuming()


def start_consumer_in_background() -> None:
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
