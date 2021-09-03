import paho.mqtt.client as mqtt
from paho.mqtt.client import *
import time

class RelayConfigCLI:

    TOPIC_CONFIG = "relay.configuration"
    MQTT_URL = "mqtt.b-iot.ch"
    MQTT_PORT = 443
    CERTIFICATE_PATH = "./isrgrootx1.pem"

    def __init__(self):
        self.quit = False

        self.relayID = "relay_biot"
        self.mqttID = "relay_biot"
        self.mqttUsername = "relayBiot_relay_biot"
        self.mqttPassword = "1049951da8f30def080f2a502d7708027905754813d624a5c72d38bda03a4a11"

        self.mqttClient = None

        print("Welcome to the Biot Relay Configurator CLI!")


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect_mqtt(self, client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.TOPIC_CONFIG, 1)

    def on_disconnect(self, client, userdata, rc):
        client.reconnect()

    # The callback for when a PUBLISH message is received from the server.
    def on_message_mqtt(self, client, userdata, msg):
        if msg.topic == self.TOPIC_CONFIG:
            print("Message = " + msg.payload.decode("utf-8"))     

    
    def connect_mqtt(self):
        # Connect the client to mqtt:
        self.mqttClient = mqtt.Client(client_id=self.mqttID, clean_session=True, userdata=None, protocol=MQTTv311, transport="websockets")
        self.mqttClient.will_set("will", payload="{\"company\": \"biot\"}", qos=0, retain=False)
        self.mqttClient.username_pw_set(self.mqttUsername, self.mqttPassword)
        # Comment to use WS without SSL
        self.mqttClient.tls_set(ca_certs=self.CERTIFICATE_PATH) 
        self.mqttClient.on_connect = self.on_connect_mqtt
        self.mqttClient.on_message = self.on_message_mqtt

        flag_error = True
        while flag_error:
            try:
                self.mqttClient.connect(self.MQTT_URL, port=self.MQTT_PORT, keepalive=60)
                flag_error = False
            except:
                print("Cannot connect, probably due to lack of network or server not responding. Wait and retry...")
                flag_error = True
                time.sleep(1)
        
        self.mqttClient.loop_start()




if __name__ == "__main__":
    cli = RelayConfigCLI()
    cli.connect_mqtt()
    while not cli.quit:
        i = input("Press q + Enter to quit:\n")
        if "q" in i or "Q" in i:
            cli.quit = True