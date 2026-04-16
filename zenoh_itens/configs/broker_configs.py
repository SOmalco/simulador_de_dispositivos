import random

zenoh_broker_configs = {
    'number_of_pub_threads': 4,
    "number_of_sub_threads": 1,
    'broker_address': 'tcp/192.168.1.11:7447',
    "id": "malco-desktop-publisher",
    "HOST": "localhost",
    "PORT": 1883,
    "CLIENT_NAME": "malco_desktop",
    "KEPPALIVE": 3,
    "topic": "esp32/public/test",
    'number_of_messages': 10,
    "messages_interval": (random.randint(1, 10))
}