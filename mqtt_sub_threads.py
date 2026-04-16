import threading
from  mqtt.mqtt_sub import mqtt_start_sub
from mqtt.configs.broker_configs import mqtt_broker_configs

number_of_threads = mqtt_broker_configs['number_of_sub_threads']
quantity = list(range(0, number_of_threads))
thread_names = []

for i in quantity:
    thread_names.append(f"Thread-{i}")

threads = list(map(lambda x: threading.Thread(target=mqtt_start_sub,
                                              args=(x, )),
                   thread_names))

list(map(lambda x: x.start(), threads))
list(map(lambda x: x.join(), threads))