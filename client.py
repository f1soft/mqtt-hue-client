"""pylint option block-disable"""

import os
import json
import requests
import paho.mqtt.client as mqtt

# Constants
INPUT_TOPIC_NAME = 'awsiot_to_localgateway'
HUE_API_IP = os.environ['HUE_API_IP']
HUE_API_USER = os.environ['HUE_API_USER']
HUE_API_BASE = 'http://' + HUE_API_IP + '/api/' + HUE_API_USER + '/'

# Service clients
MQTT_CLIENT = mqtt.Client()

def on_connect(client, userdata, flags, result):
    """Subscribe to input topic"""

    print('Connected ' + str(result))

    print('Subscribing to ' + INPUT_TOPIC_NAME)
    MQTT_CLIENT.subscribe(INPUT_TOPIC_NAME)

    print('Using Hue API ' + HUE_API_IP + ' with user ' + HUE_API_USER)


# Operations for message handler
def get_state():
    """Get state of all lights"""
    request_url = HUE_API_BASE + 'lights/'
    print('Request: ' + request_url)
    response = requests.get(request_url).json()
    return response


# Map of operation (from topic) to handler function
OPERATION_FUNCTION_MAP = {
    'getState': get_state
}


def on_message(mqtt_client, userdata, message):
    """Handle messages"""

    print('Received message: ' + str(message.payload))
    payload = json.loads(message.payload)
    operation = payload['operation']

    response = OPERATION_FUNCTION_MAP[operation]()
    print('Response: ' + str(response))
    

def main(): # pylint: disable=C0111
    MQTT_CLIENT.on_connect = on_connect
    MQTT_CLIENT.on_message = on_message

    MQTT_CLIENT.connect('localhost', 1883)
    MQTT_CLIENT.loop_forever()


if __name__ == '__main__':
    main()
