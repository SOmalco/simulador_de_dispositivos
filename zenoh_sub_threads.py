import threading
from zenoh_itens.zenoh_sub import zenoh_start_sub
from zenoh_itens.configs.broker_configs import zenoh_broker_configs

number_of_threads = zenoh_broker_configs['number_of_sub_threads']
quantity = list(range(0, number_of_threads))
thread_names = []

for i in quantity:
    thread_names.append(f"Thread-{i}")

threads = list(map(lambda x: threading.Thread(target=zenoh_start_sub,
                                              args=(x, )),
                   thread_names))

list(map(lambda x: x.start(), threads))
list(map(lambda x: x.join(), threads))