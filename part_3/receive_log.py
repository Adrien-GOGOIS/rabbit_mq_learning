import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Ici on laisse queue vide pour récupérer un queue random qui sera détruite après le log consommé
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

# Enregistrer les logs dans un fichier : - python receive_log.py > logs_from_rabbit.log
# Afficher les logs : - python receive_log.py / python emit_log.py

# Utiliser : - sudo rabbitmqctl list_bindings
# Avec 2 receive_log.py ouvert, on verra 2 noms de queue aléatoires différents
