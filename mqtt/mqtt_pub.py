import csv
import datetime
import random
import time
import paho.mqtt.client as mqtt
from .configs.broker_configs import mqtt_broker_configs

def mqtt_publisher(thread_name):
    client_id = mqtt_broker_configs["id"]
    endpoint = mqtt_broker_configs["HOST"]
    port = mqtt_broker_configs["PORT"]
    topic = mqtt_broker_configs["topic"]
    intervalo = mqtt_broker_configs["messages_interval"]

    # --- Main Program ---
    print("--- MQTT Publisher ---")
    print(f"I am a MQTT-Publisher!")
    print(f"Connecting to: {endpoint}:{port}")
    print(f"Publishing on Topic: {topic}\n")

    print("Opening session...")
    pub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, 'malco-desktop')
    pub.connect(host=endpoint, port=port)

    csv_file = [['send_time', 'client_id', 'thread_name', '# of message']]
    value_counter = 0
    print(f"\nStart publishing every {intervalo} seconds...")
    while value_counter < 10:
        time.sleep(intervalo)
        try:
            horario = datetime.datetime.now()
            message =  f"{horario},{client_id},{thread_name},{value_counter}"
            print(f" >>> Sending: '{message}'")
            pub.publish(topic=topic, payload=message)
            row = message.split(",")
            csv_file.append(row)
            value_counter += 1

        except KeyboardInterrupt:
            break

    # --- Cleanup ---
    print("\nClosing session...")
    pub.disconnect()

    # print(csv_file)
    # with open(f'mqtt-csvs/1_Threads/{thread_name}-Mqtt.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(csv_file)  # Write header

