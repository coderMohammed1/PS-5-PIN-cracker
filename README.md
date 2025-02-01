# PS-5-PIN-cracker
this repository explain the exploitation of HDMI-CEC to programmatically control a ps 5, helping you to bruteforce ps5 pins!  

# IMPORTANT

the codes provided only works for some samsung tves with an api to control them and a support of HDMI-CEC. However the showen method can be exploited with any HDMI-CEC supported TV!

---

# Technical description:

## Summary
This report demonstrates a method to programmatically control a PlayStation 5 (PS5) using Python, leveraging the HDMI-CEC capabilities of Samsung Smart TVs. It further shows how this method can be utilized to brute force PINs of local PS5 accounts without encountering rate limits.

---

## Background
The idea for this exploration began with an interest in remotely controlling the PS5 programmatically. Initial attempts to use PS5 controller protocols were met with limitations, as they were not designed for this use case. The breakthrough came from observing the use of a Samsung Smart TV remote to control the PS5 via HDMI-CEC, which allowed us to explore control using Samsung's APIs.

---

## Discovery Process

### Initial Attempt
An attempt was made to utilize existing PlayStation controller libraries and remote protocols, but these methods proved unsuitable due to their restricted functionality in bypassing PIN-protected accounts.

### Second Attempt
The discovery that a Samsung Smart TV remote could control the PS5 inspired the idea of programmatically controlling the TV to indirectly manage the PS5. Research into Samsung's Smart TV APIs revealed existing libraries and user contributions, which were refined and adapted for this purpose.

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

bservations

The script successfully brute-forced a PS5 account PIN without encountering rate limits or other protective mechanisms. This exposes a critical vulnerability in PS5's account security when paired with HDMI-CEC-enabled TVs.

# Impacts

1- PIN bypass

2- ps5 limited remote control  

3- may be further utilized for more malicious usages and not only a pin guess.

4- this way may impact other devices as well, as this provide a general way of automating device control.

## Conclusion

This report outlines a novel method for leveraging Samsung Smart TV APIs and HDMI-CEC to programmatically control a PS5 using Python.

**Note**: This demonstration is intended for ethical and research purposes only.
