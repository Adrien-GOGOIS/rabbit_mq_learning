import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

# Maintenant nous sommes prêts pour envoyer un message plus complexe
message = ' '.join(sys.argv[1:]) or "Hello World"

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(f" [x] Sent {message}")

# Ne pas oublier de fermer la connexio ensuite
connection.close()
