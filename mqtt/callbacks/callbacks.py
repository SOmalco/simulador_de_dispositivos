import csv
import datetime
import pandas as pd
from mqtt.configs.broker_configs import mqtt_broker_configs

class MessageList:
    def __init__(self):
        self.shared_list = []
    def add(self, num):
        self.shared_list.append(num)

list1 = MessageList()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Cliente Conectado com sucesso: {client._client_id}')
        client.subscribe(mqtt_broker_configs["topic"])

    else:
        print(f'Erro ao me conectar! codigo={rc}')


def on_subscribe(client, userdata, mid, granted_qos):
    print(f'Client Subscribed at {mqtt_broker_configs["topic"]}')
    print(f'QOS: {granted_qos}')


def on_message(client, userdata, message):
    horario = str(datetime.datetime.now())
    message = message.payload.decode("utf-8").split(',')
    thread = message[2]
    message.append(horario)
    list1.add(message)

    if len(list1.shared_list) > 9:
        df =  pd.DataFrame(list1.shared_list, columns=['send_time', 'client_id', 'thread_name', '# of message', 'received_time'])
        df.to_csv(f'mqtt-csvs/{thread}.csv', index=False)
