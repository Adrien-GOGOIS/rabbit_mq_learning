import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Appeler une queue durable (on change le nom car erreur si création d'une queue avec le même nom):
# Evite de perdre les messages si serveur down
channel.queue_declare(queue='task_queue', durable=True)

# Maintenant nous sommes prêts pour envoyer un message plus complexe
message = ' '.join(sys.argv[1:]) or "Hello World"

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE  # Fonctionne avec queue "durable"
                      ))

print(f" [x] Sent {message}")

# Ne pas oublier de fermer la connexio ensuite
connection.close()
