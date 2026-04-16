import datetime
from .configs.broker_configs import zenoh_broker_configs
import zenoh
import time
import pandas as pd

# --- Configuration ---
# Define connection details
endpoint = zenoh_broker_configs['broker_address']
key = zenoh_broker_configs['topic']

class MessageList:
    def __init__(self):
        self.shared_list = []
    def add(self, num):
        self.shared_list.append(num)

list1 = MessageList()

# --- Functions ---
def listener(sample):
    """Callback function to handle incoming messages."""
    horario = str(datetime.datetime.now())
    message = bytes(sample.payload).decode('utf-8').split(',')
    thread = message[2]
    message.append(horario)
    list1.add(message)

    if len(list1.shared_list) > 9:
        df =  pd.DataFrame(list1.shared_list, columns=['send_time', 'client_id', 'thread_name', '# of message', 'received_time'])

        df.to_csv(f'zenoh-csvs/{thread}.csv', index=False)

# --- Main Program ---
print("--- Zenoh Subscriber ---")
print(f"I am a Subscriber")
print(f"Connecting to: {endpoint}")
print(f"Subscribing to Key: {key}\n")


def zenoh_start_sub(thread_name=None):

    # Create a Zenoh config object
    conf = zenoh.Config()
    conf.insert_json5("connect", f'{{"endpoints": ["{endpoint}"]}}')

    print("Opening session...")
    session = zenoh.open(conf)

    print(f'Client Subscribed at {key}')
    sub = session.declare_subscriber(key, listener)

    print("\nWaiting for messages... Press Ctrl+C to quit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # --- Cleanup ---
    print("\nClosing session...")
    sub.undeclare()
    session.close()

if __name__ == "__main__":
    start()
