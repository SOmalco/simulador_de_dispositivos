import threading
from zenoh_itens.configs.broker_configs import zenoh_broker_configs
from zenoh_itens.zenoh_pub import publisher

number_of_pubs = zenoh_broker_configs['number_of_pub_threads']
quantity = list(range(0, number_of_pubs))
thread_names = []

for i in quantity:
    thread_names.append(f"Thread-{i}")

threads = list(map(lambda x: threading.Thread(target=publisher,
                                              args=(x, )),
                   thread_names))

list(map(lambda x: x.start(), threads))
list(map(lambda x: x.join(), threads))