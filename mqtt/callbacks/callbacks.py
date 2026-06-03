import datetime
import pandas as pd
from mqtt.configs.broker_configs import mqtt_broker_configs

class MessageList:
    def __init__(self):
        self.shared_list = {}
        number_of_threads = mqtt_broker_configs['number_of_sub_threads']
        for thread_n in range(number_of_threads):
            self.shared_list[f'Thread-{thread_n}'] = []
    def add(self, thread_n, thread_message):
       self.shared_list[thread_n].append(thread_message)

list1 = MessageList()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Cliente Conectado com sucesso: {client._client_id}\n')

    else:
        print(f'Erro ao me conectar! codigo={rc}')


def on_subscribe(client, userdata, mid, granted_qos):
    print(f'QOS: {granted_qos}')

def on_disconnect(client, userdata, mid, granted_qos):
    print(f'Client Disconnected')

def on_message(client, userdata, message):
    horario = str(datetime.datetime.now())
    message = message.payload.decode("utf-8").split(',')
    if mqtt_broker_configs['number_of_pub_threads'] ==1:
        thread = client._client_id[-8:].decode('utf-8')
    else:
        thread = message[2]
    message.append(horario)
    list1.add(thread, message)

    print(f"client: {client._client_id} thread: {thread} lista: {list1.shared_list}")
    if len(list1.shared_list[thread]) > 9:
        df = pd.DataFrame(list1.shared_list[thread],
                          columns=['send_time', 'client_id', 'thread_name', '# of message', 'received_time'])
        df.to_csv(f'mqtt-csvs/{thread}.csv',
                  index=False)
