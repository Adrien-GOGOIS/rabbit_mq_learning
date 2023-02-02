import os
import sys
import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='temperature')

    def callback(channel, method, properties, body):
        temperature = int(body)
        print(f"Température reçue : {temperature}°C")
        if temperature >= 25:
            print("Démarrage du ventilateur...")
        else:
            print("Ventilateur à l'arrêt")

    channel.basic_consume(queue='temperature',
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Démarrage du programme, en attente de relevé de température. Quitter : CTRL+C')
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
