import random
import zenoh
import time
import datetime
import csv
from .configs.broker_configs import zenoh_broker_configs

def publisher(thread_name):
    # --- Configuration ---
    # Define connection details
    endpoint = zenoh_broker_configs['broker_address']
    key = zenoh_broker_configs['topic']

    # Create a Zenoh config object
    conf = zenoh.Config()
    conf.insert_json5("connect", f'{{"endpoints": ["{endpoint}"]}}')

    # --- Main Program ---
    print("--- Zenoh Publisher ---")
    print(f"I am a Publisher!")
    print(f"Connecting to: {endpoint}")
    print(f"Publishing on Key: {key}\n")

    print("Opening session...")
    session = zenoh.open(conf)

    intervalo = zenoh_broker_configs['messages_interval']

    print(f"Declaring publisher for key expression '{key}'...")
    pub = session.declare_publisher(key)

    csv_file = [['send_time', 'client_id', 'thread_name', '# of message']]
    value_counter = 0
    print(f"\nStart publishing every {intervalo} seconds...")
    while value_counter < zenoh_broker_configs['number_of_messages']:
        time.sleep(intervalo)  # Send a message every "intervalo" seconds
        try:
            horario = datetime.datetime.now()
            message =  f"{horario},{pub.id.zid},{thread_name},{value_counter}"
            print(f" >>> Sending: '{message}'")
            pub.put(message)
            row = message.split(",")
            csv_file.append(row)
            value_counter += 1
        except KeyboardInterrupt:
            break

    # --- Cleanup ---
    print("\nClosing session...")
    pub.undeclare()
    session.close()

    print(csv_file)
    # with open(f'zenoh-csvs/{thread_name}-zenoh.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(csv_file)  # Write header

