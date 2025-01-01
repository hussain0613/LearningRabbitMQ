import pika
import pika.channel

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print("ch:", ch, type(ch))
    print("method:", method, type(method))
    print("properties:", properties, type(properties))
    print("body:", body, type(body))
    print(f" [x] Received {body}")

channel.basic_consume(
    queue='hello',
    auto_ack=True,
    on_message_callback=callback,
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
