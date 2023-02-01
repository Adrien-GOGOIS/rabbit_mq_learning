import os
import sys
import pika


def main():
    # Etablir la connexion avec le serveur RabbitMQ :
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Machine locale ici, sinon mettre nom
    # ou adresse IP
    channel = connection.channel()

    # Créer une queue (sinon le message sera automatiquement jeté) :
    channel.queue_declare(queue='hello')

    # Pour recevoir les messages de la queue, il faut utiliser un callback
    def callback(channel, method, properties, body):
        print(f"Received {body}")

    # Puis on indique que cette fonction est censé recevoir des messages depuus la queue "hello" :
    channel.basic_consume(queue='hello',
                          auto_ack=True,  # A voir plus tard
                          on_message_callback=callback)  # Fonction : qu'est-ce qu'on fait de ce message ?

    # Puis on crée une boucle pour attendre les nouveaux messages qui catch "keyboard interrupt" pour l'arrêter :
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

# OUVRIR 2 TERMINALS :
    # python receive.py
    # Puis python send.py
