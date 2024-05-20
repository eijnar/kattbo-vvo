import pika

credentials = pika.PlainCredentials('vvo_celery', 'mjykq5zx98tqgm9szou6')
parameters = pika.ConnectionParameters('172.30.149.76',
                                       5672,
                                       'kattbo_vvo',
                                       credentials)

try:
    connection = pika.BlockingConnection(parameters)
    print("Connection to RabbitMQ successful!")
    connection.close()
except Exception as e:
    print(f"Connection to RabbitMQ failed: {e}")
