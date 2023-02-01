import pika

# Etablir la connexion avec le serveur RabbitMQ :
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # Machine locale ici, sinon mettre nom
# ou adresse IP
channel = connection.channel()

# Créer une queue (sinon le message sera automatiquement jeté) :
channel.queue_declare(queue='hello')

# Maintenant nous sommes prêts pour envoyer un message.
# Avec RabbitMQ, les messages doivent d'abord transiter par un "exchange", on va commencer par un exchange par defaut
channel.basic_publish(exchange='',  # Exchange spécial "" qui permet de spécifier directement le nom de la queue
                      routing_key='hello',  # Nom de la queue
                      body='Bonjour le Monde')  # Message

# Ne pas oublier de fermer la connexio ensuite
connection.close()

# Voir le nombre de messages dans la queue : - sudo rabbitmqctl list_queues


