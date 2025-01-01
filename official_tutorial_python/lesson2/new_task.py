import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="task_queue",
    durable=True, # To ensure that the queue won't be lost even if RabbitMQ restarts/crashes, however, messages will still be lost if RabbitMQ crashes before it saves the message to disk.
                    # so not 100% guaranteed (?!?)
)

msg = " ".join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=msg,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent, # Marks the message as persistent
    )
)

print(f" [x] Sent '{msg}'")

connection.close()
