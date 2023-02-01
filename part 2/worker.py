import os
import sys
import time

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Créer une queue durable (on change le nom car erreur si création d'une queue avec le même nom):
    # Evite de perdre les messages si serveur down
    channel.queue_declare(queue='task_queue', durable=True)

    # Pour chaque point de suspension contenu dans le message, on feint une seconde de travail :
    def callback(channel, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='hello',
                          # auto_ack=True,
                          on_message_callback=callback)
    # auto-ack = Acknowledgments : renvoie un message au boroker "message bien reçu".
    # Si un consumer se ferme avant la fin d'un message, RabbitMQ est au courant et pourra essayer un autre consumer
    # On l'avait éteint avec auto_ack=True, on rajoute plutôt "channel.basic_ack(delivery_tag=method.delivery_tag)"

    # Debug : - sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except:
            os._exit(0)

# TESTER avec 3 consoles:
# - python worker.py
# - python worker.py
# - python new_task.py First message.
#   python new_task.py Second message..
#   python new_task.py Third message...
#   python new_task.py Fourth message....
#   python new_task.py Fifth message.....

# Par defaut, RabbitMQ va passer d'un consumer à l'autre pour distribuer les messages comme des cartes une par une
