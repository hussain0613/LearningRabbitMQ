import sys
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare( 
    exchange="logs", # The name of the exchange, "" is a default exchange, which is a direct exchange with no name (empty string)
    exchange_type="fanout", # The fanout exchange. It just broadcasts all the messages it receives to all the queues it knows.
)

msg = " ".join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(
    exchange="logs",
    routing_key="", # The value of the `routing_key` parameter is ignored for `fanout` exchanges, so we can just set it to an empty string.
    body=msg,
)
# The message goes to the exchange, and the fanout exchange will broadcast it to all known queues.

print(f" [x] Sent '{msg}'")

connection.close()
