import time
import uuid
import paho.mqtt.client as mqtt
from .configs.broker_configs import mqtt_broker_configs
from .callbacks.callbacks import on_connect, on_subscribe, on_message, on_disconnect
from mqtt.callbacks.callbacks import MessageList

class MqttClientConnection:
    def __init__(self,
                 broker_ip: str,
                 port: int,
                 client_name: str,
                 keepalive=60,
                 thread_name=None):
        self.__broker_ip = broker_ip
        self.__port = port
        self.__client_name = client_name
        self.__keepalive = keepalive
        self.__mqtt_client = None
        self.__thread_name = thread_name

    def start_connection(self, thread_name):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,
                                  client_id=self.__client_name)

        # callbacks
        mqtt_client.on_connect = on_connect
        mqtt_client.on_subscribe = on_subscribe
        mqtt_client.on_message = on_message
        mqtt_client.on_disconnect = on_disconnect

        mqtt_client.connect(host=self.__broker_ip,
                            port=self.__port,
                            keepalive=self.__keepalive)
        mqtt_client.subscribe(thread_name)
        print(f"client on port {self.__port} subscribed to {thread_name}")

        # self.__mqtt_client = mqtt_client
        # self.__mqtt_client.loop_start()
        mqtt_client.loop_start()

    def end_conn(self):
        try:
            print("DISCONNECTING")
            self.__mqtt_client.loop_stop()
            self.__mqtt_client.loop_stop()
            self.__mqtt_client.disconnect()
            return True
        except:
            return False

def mqtt_start_sub(thread_name=None):
    print(f"Starting MQTT Subscriber...{thread_name}")
    mqtt_client_connection = MqttClientConnection(broker_ip=mqtt_broker_configs["HOST"],
                                                  port=mqtt_broker_configs["PORT"],
                                                  client_name=mqtt_broker_configs["CLIENT_NAME"]+thread_name,
                                                  keepalive=mqtt_broker_configs["KEPPALIVE"],
                                                  thread_name=thread_name)
    mqtt_client_connection.start_connection(thread_name)

    while True:
        time.sleep(0.001)

if __name__ == "__main__":
    mqtt_start_sub()
