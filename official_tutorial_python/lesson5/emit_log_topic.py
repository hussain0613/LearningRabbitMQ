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
# The exchange type is 'topic' instead of 'direct'
# This allows for more complex routing patterns instead of just routing keys

# Routing key can now take the form of a list of words separated by dots
# The words can be anything, but usually they are related to the message content
# The routing key can now contain wildcards:
# * (star) can substitute for exactly one word
# # (hash) can substitute for zero or more words

routing_key = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"

msg = " ".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(
    exchange="topic_logs",
    routing_key=routing_key,
    body=msg,
)

print(f" [x] Sent {routing_key}: {msg}")

connection.close()

