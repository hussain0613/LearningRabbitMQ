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

severity = sys.argv[1] if len(sys.argv) > 1 else "info"

msg = " ".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(
    exchange="direct_logs",
    routing_key=severity,
    body=msg,
)

print(f" [x] Sent '{severity}':'{msg}'")

connection.close()

