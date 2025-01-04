import pika

with pika.BlockingConnection(pika.ConnectionParameters('localhost')) as connection:
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    msg = "Hello World, Again!"

    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=msg,
    )

    print(f" [x] Sent '{msg}'")
