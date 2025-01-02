import sys
import pika
import pika.connection

connection = pika.BlockingConnection(
    parameters = pika.connection.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="topic_logs",
    exchange_type="topic",
)


result = channel.queue_declare(
    queue="",
    exclusive=True,
)

queue_name = result.method.queue

binding_keys = sys.argv[1:] if len(sys.argv) > 1 else ["anonymous.info"]
# The binding keys are the routing keys that the consumer will use to bind the queue to the exchange
# Exampls of binding keys for this exchange type:
# "anonymous.info"
# "anonymous.*" - Will receive all messages tagged with two words where first word is 'anonymous'
# "*.info" - Will receive all messages tagged with two words where second word is 'info'
# "anonymous.#" - Will receive all messages tagged with one or more words where first word is 'anonymous'
# "#" - Will receive all messages

for binding_key in binding_keys:
    channel.queue_bind(
        exchange="topic_logs",
        queue=queue_name,
        routing_key=binding_key,
    )

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
