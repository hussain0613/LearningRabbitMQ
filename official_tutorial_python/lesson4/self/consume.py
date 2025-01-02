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

queue_name = "logs"
result = channel.queue_declare(
    queue=queue_name,
    durable=True,
)
queue_name = result.method.queue

severities = sys.argv[1:] or ["info"]

for severity in severities:
    channel.queue_bind(
        exchange="direct_logs",
        queue=queue_name,
        routing_key=severity,
    )

# Will receive messages from the 'logs' queue with the routing key provided in the command line argument

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(
    ch, 
    method, 
    properties, 
    body
):
    print(f" [x] {method.routing_key}: {body}")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()

