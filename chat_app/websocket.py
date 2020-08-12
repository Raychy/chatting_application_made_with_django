# """Receive messages over from RabbitMQ and send them over the websocket."""

import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.exchange_declare(
    exchange='fe662fd9de834fc', exchange_type='fanout'
)

# exclusive means the queue should be deleted once the connection is closed 
result = channel.queue_declare(exclusive=True, queue = 'hello')
queue_name = result.method.queue  # random queue name generated by RabbitMQ 
channel.queue_bind(exchange='fe662fd9de834fc', queue=queue_name)

print('listening for messages...')

while True:
    for method_frame, _, body in channel.consume(queue_name):
        try:
            print(body)
        except OSError as error:
            print(error)
        else:
            # acknowledge the message             
            channel.basic_ack(method_frame.delivery_tag)