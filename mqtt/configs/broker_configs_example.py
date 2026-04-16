import random

mqtt_broker_configs = {
    "number_of_pub_threads": 3,
    "number_of_sub_threads": 1,
    "id": "",
    "HOST": "localhost",
    "PORT": 1883,
    "CLIENT_NAME": "",
    "KEPPALIVE": 3,
    "topic": "test",
    'number_of_messages': 10,
    "messages_interval": 1#random.randint(1, 10)
}