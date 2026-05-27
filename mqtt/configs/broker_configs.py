import random

mqtt_broker_configs = {
    "number_of_pub_threads": 5,
    "number_of_sub_threads": 5,
    "id": "malco-desktop-publisher",
    "HOST": "localhost",
    "PORT": 1883,
    "CLIENT_NAME": "malco_desktop",
    "KEPPALIVE": 30,
    "topic": "test",
    'number_of_messages': 10,
    "messages_interval": 1  # random.randint(1, 10)
}
