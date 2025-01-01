import time
import pika

from pika.adapters.blocking_connection import BlockingChannel
from pika import spec

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="task_queue",
    durable=True, # To ensure that the queue won't be lost even if RabbitMQ restarts/crashes, however, messages will still be lost if RabbitMQ crashes before it saves the message to disk.
                    # so not 100% guaranteed (?!?)
)

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(
    ch: BlockingChannel, 
    method: spec.Basic.Deliver,
    properties: spec.BasicProperties,
    body: bytes
) -> None:
    print(f" [x] Received {body}")
    timer = body.count(b'.')
    print(f" [x] Fake-working for {timer} seconds")
    time.sleep(timer)
    print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag) # Sends acknowledgement(ack) to the RMQ server that the message has been received and processed


# Quality of Service (QoS) settings
channel.basic_qos(prefetch_count=1) # This tells RabbitMQ not to give more than one message to a worker at a time.
                                    # Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
                                    # Instead, it will dispatch it to the next worker that is not still busy.

channel.basic_consume(
    queue="task_queue",
    on_message_callback=callback,
)

channel.start_consuming() # This is a blocking call that will wait for messages from the server.
                            # It will run the callback function whenever a message is received.

