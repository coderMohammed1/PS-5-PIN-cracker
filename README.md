# PS-5-PIN-cracker
this repository explains the exploitation of HDMI-CEC to programmatically control a ps 5, helping you to bruteforce ps5 pins!  

# IMPORTANT

the codes provided only works for some samsung tves with an api to control them and a support of HDMI-CEC. However the showen method can be exploited with any HDMI-CEC supported TV!

---

# for users:

a more user friendly version has been created. you can find the instructions in the release folder!

# Technical description:

## Summary
This repository demonstrates a method to programmatically control a PlayStation 5 (PS5) using Python, leveraging the HDMI-CEC capabilities of Samsung Smart TVs. It further shows how this method can be utilized to brute force PINs of local PS5 accounts without encountering rate limits.

---

#### Key Steps:
1. Scanned the TV's network ports using Nmap, identifying port `8002` as a potential entry point.
2. Used Python to establish a WebSocket connection and authenticate using a generated token.
3. Implemented a script to simulate PIN entry sequences, leveraging the TV's control over the PS5.
Note: those steps might differ from TV to other. Some TVs does not require you to touch them to do the whole exploit.
---

## Nmap Scan Results
The following is an excerpt from the Nmap scan results for the Samsung Smart TV:

```bash
Nmap scan report for 192.168.1.119
Host is up (0.0026s latency).
PORT      STATE  SERVICE
8002/tcp  open   ssl/teradataordbms?
```

## Prerequisites

- A TV with HDMI-CEC support.
- The ability to control the PS5 with the TV remote.
- Python 3 installed along with the following libraries:
    - `base64`
    - `json`
    - `logging`
    - `time`
    - `ssl`
    - `websocket`

Install dependencies using `pip install [requirement name]`.


## Implementation Steps

1. **Prepare the Setup**:
    
    - Ensure the TV can control the PS5 via HDMI-CEC.
    - Start the PS5 by powering on the TV. (in my case I needed to power on the ps 5 using the TV remote and not the controller)
		Note: you may need to try this multiple times depending on the TV.
    
2. **Token Retrieval**:
    
    - Use the provided Python script (token.py) to retrieve an authentication token from the TV.

3. **PIN bypass**


	go to the account you want to brute force click on it and then run pin.py


# use cases

1- PIN bypass

2- ps5 limited remote control  

3- may be further utilized for more malicious usages and not only a pin guess.

4- this way may impact other devices as well, as this provide a general way of automating device control.


**Note**: This demonstration is intended for ethical and research purposes only.
