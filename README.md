
# Packet Interception Kernel Module (Raspberry Pi Communication)

This project implements a Linux kernel module that uses Netfilter to intercept TCP packets containing a specific password. Once authenticated, it logs incoming payloads from that source. The system is designed to enable secure, password-activated communication between a host computer and a **Raspberry Pi**.

## Use Case

This module is ideal for lightweight, password-triggered communication with embedded systems—specifically, a Raspberry Pi. Upon receiving a special password via TCP, the host machine enters “interception mode,” listening and logging further packets from the Pi.

##  Features

- Password-based trigger to initiate logging  
- Intercepts and logs TCP payloads from a specified source (the Pi)  
- Custom Python scripts included for packet crafting and testing  
- Easy to build and deploy on Linux systems  
- Can run on machines communicating with a Raspberry Pi over a local network  

##  Project Structure

| File | Purpose |
|------|---------|
| `Module.c` / `Module-CPY.c` | Core Netfilter kernel module to intercept TCP packets |
| `Makefile-Cpy` | Makefile for building the kernel module |
| `PacketSend.py` | Sends TCP packets to the host, simulating communication from the Pi |
| `dMsg.py`, `dMsg-CPY.py` | Message formatting or secondary send/receive tools |
| `test.py`, `test-copy.py`, `second.py` | Unit tests and helper scripts |
| `hudson@172.16.64.147` | Possibly saved SSH config/session for the Raspberry Pi |


1. Raspberry Pi sends a TCP packet containing a password (e.g. `"pass"`).
2. Host kernel module detects the password and switches into intercept mode.
3. After that, all future TCP messages from the Pi's port and IP are recorded directly in the kernel message log.

##  Getting Started

```bash
make -f Makefile-Cpy
sudo insmod Module.ko
dmesg | tail
```

Use `PacketSend.py` or the Raspberry Pi to send a password-authenticated message.

To remove the module:

```bash
sudo rmmod Module
```

---

## Quickstart Instructions

###  On the Host (Linux Machine)

1. **Build the kernel module**
    ```bash
    make -f Makefile-Cpy
    ```

2. **Insert the module**
    ```bash
    sudo insmod Module.ko
    dmesg | tail
    ```

3. **(Optional) Modify the password**  
   In `Module.c`, change:
    ```c
    #define GREENDAY "pass"
    ```
   Then rebuild.

4. **Start logging**
    - Use `PacketSend.py` to send the password:
      ```bash
      python3 PacketSend.py <raspi_ip> <port> "pass"
      ```

    - After password is detected, any future messages from the Pi's IP/port will appear in the kernel log:
      ```bash
      dmesg -w
      ```

---

###  On the Raspberry Pi

1. **Send test payload using netcat**
    ```bash
    echo "pass" | nc <host_ip> <port>
    echo "follow-up msg" | nc <host_ip> <port>
    ```

3. **Watch logs on host**
    ```bash
    dmesg -w
    ```

---

