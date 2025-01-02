import sys
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()


channel.exchange_declare(
    exchange="direct_logs",
    exchange_type="direct",
)

channel.queue_declare(
    queue="logs",
    durable=True,
)


severity = sys.argv[1] if len(sys.argv) > 1 else "info"

channel.queue_bind( # This will bind the 'logs' queue to the 'direct_logs' exchange with the routing key provided in the command line argument
    exchange="direct_logs",
    queue="logs",
    routing_key=severity,
)

msg = " ".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(
    exchange="direct_logs",
    routing_key=severity, # This will send the message to the exchange with the routing key provided in the command line argument
    body=msg,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,
    )
)
# Publisher doesn't know about queues, it just sends messages to exchanges, specifying a routing key
# The exchange then decides what to do with the message, generally it will be sent to the queue with that contains the routing key
# It seems, if routing key is same as the queue name, the message will be sent to that queue

# Consumer binds the queue to the exchange, specifying the routing key, so that it will receive messages with that routing key

# Here, declaring the queue and binding it to the exchange ensures that even if the consumer is not running, the message will be saved in the queue
# and will be delivered to the consumer when it starts running
# If the queue is not declared and bound to the exchange, the message will be dropped if the consumer is not running with the correct routing key

print(f" [x] Sent '{msg}'")

connection.close()

