import os
import random
import sys
import time

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='temperature')


def send_temperature():
    print("Relevé de température...")
    time.sleep(5)
    temperature = random.randint(0, 40)
    print(f"Nouvelle température : {temperature}°C")
    channel.basic_publish(exchange='',
                          routing_key='temperature',
                          body=str(temperature))
    send_temperature()


try:
    send_temperature()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except:
        os._exit(0)

connection.close()
