import os

from typing import Optional, Callable
from datetime import datetime

from paho.mqtt.client import Client, MQTT_ERR_NO_CONN

# Configuration data
HOST = "perfect-gardener.cloudmqtt.com"
PORT = 1883
USERNAME = os.environ.get("MQTT_USERNAME")
PASSWORD = os.environ.get("MQTT_PASSWORD")


# Initialize and connect
def initialize_client(client_id: str) -> Client:
    paho_client = Client(client_id=client_id)
    paho_client.username_pw_set(username=USERNAME, password=PASSWORD)
    paho_client.connect(HOST, PORT)
    paho_client.loop_start()
    return paho_client


# Stop connection
def stop_connection(paho_client: Client) -> None:
    paho_client.loop_stop()
    paho_client.disconnect()


# Register a callable function to trigger when a client successfully connects to the configured broker
def register_on_connect_callback(paho_client: Client, callback: Optional[Callable]) -> None:
    paho_client.on_connect = callback


# Subscribe to a channel with two parameters topic and quality of service
def subscribe_to_channel(paho_client: Client, topic: str, qos: int = 0) -> None:
    paho_client.subscribe(topic=topic, qos=qos)


# Register a callable function to trigger everytime a new message is received
def register_on_message_callback(paho_client: Client, callback: Optional[Callable]) -> None:
    paho_client.on_message = callback


# Publish message to a channel
def publish_to_channel(paho_client: Client, message: str, topic: str, qos: int = 0) -> None:
    rc = paho_client.publish(payload=message, topic=topic, qos=qos)
    if rc == MQTT_ERR_NO_CONN:
        raise ConnectionRefusedError(f"Unable to publish message '{message}'. Client not connected: rc = {rc}")


# Define a function for on_massage
def on_message(client, userdata, message) -> None:
    print(f"Received message {message.payload} on topic {message.topic} with QoS {message.qos}")


if __name__ == "__main__":
    # Example how to subscribe to a channel
    topic = "ais/live/hamburg2"
    paho_client = initialize_client(client_id="some_id")
    subscribe_to_channel(paho_client=paho_client, topic=topic, qos=0)
    register_on_message_callback(paho_client=paho_client, callback=on_message)
    now = datetime.now()
    while (datetime.now()-now).seconds <= 10:
        pass
    stop_connection(paho_client=paho_client)

    # Example how to publish a message
    topic = "MHT/my-topic"
    message = "Example message"
    paho_client = initialize_client(client_id="some_id")
    subscribe_to_channel(paho_client=paho_client, topic=topic, qos=0)
    register_on_message_callback(paho_client=paho_client, callback=on_message)
    publish_to_channel(paho_client=paho_client, message=message, topic=topic, qos=2)
    now = datetime.now()
    while (datetime.now() - now).seconds <= 10:
        pass
    stop_connection(paho_client=paho_client)
