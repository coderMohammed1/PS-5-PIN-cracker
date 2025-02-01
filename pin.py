import base64
import json
import logging
import time
import websocket
import ssl
from websocket import create_connection

class SamsungTV:
	# replace the tokne with the one you got from the code above
    def _init_(self, host, port=8002, name="MyRemote", token="your token here"):
        uri = f"wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={base64.b64encode(name.encode('utf-8')).decode('utf-8')}"
        if token:
            uri += f"&token={token}"
        self.connection = create_connection(uri, sslopt={"cert_reqs": ssl.CERT_NONE})

        # Receive and print the response for debugging
        response = json.loads(self.connection.recv())
        print("Response from TV:", json.dumps(response, indent=4))  # Print the entire response

        if response['event'] != 'ms.channel.connect':
            self.close()
            raise Exception(f"Unexpected event: {response['event']}")

        self.token = token
    
    def _exit_(self, type, value, traceback):
        self.close()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_token(self):
        return self.token

    def send_key(self, key):
        payload = json.dumps({'method': 'ms.remote.control', 'params': {'Cmd': 'Click', 'DataOfCmd': key, 'Option': 'false', 'TypeOfRemote': 'SendRemoteKey'}})
        self.connection.send(payload)
        time.sleep(0.2)

# Use your TV's IP address here
tv = SamsungTV("192.168.1.119", token="Your token here") # ur token again 

# here is the ps5 part of it
for i in range(1,10000):
    num = f"{i:04d}"
    tv.send_key(f"KEY_{num[0]}")
    tv.send_key(f"KEY_{num[1]}")

    tv.send_key(f"KEY_{num[2]}")
    tv.send_key(f"KEY_{num[3]}")
    time.sleep(0.3)
    tv.send_key("KEY_ENTER")
    print (num)
