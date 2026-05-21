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
        self.shared_list = {}
        number_of_threads = zenoh_broker_configs['number_of_pub_threads']
        for thread_n in range(number_of_threads):
            self.shared_list[f'Thread-{thread_n}'] = []
    def add(self, thread_n, thread_message):
       self.shared_list[thread_n].append(thread_message)

list1 = MessageList()

# --- Functions ---
def listener(sample):
    """Callback function to handle incoming messages."""
    horario = str(datetime.datetime.now())
    message = bytes(sample.payload).decode('utf-8').split(',')
    print(message)
    thread = message[2]
    message.append(horario)
    list1.add(thread, message)

    if len(list1.shared_list[thread]) > 9:
        df =  pd.DataFrame(list1.shared_list[thread], columns=['send_time', 'client_id', 'thread_name', '# of message', 'received_time'])
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

    print(f'Client Subscribed at {thread_name}')
    sub = session.declare_subscriber(thread_name, listener)

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
    zenoh_start_sub()
