from scapy.all import *
from scapy.all import TCP, IP, sniff
import socket

count = 0
def packet_callback(packet):
    if packet.haslayer('TCP') and packet[TCP].sport == 5000:
        global count
        # Packet is from port 5000, perform actions here
        print(packet)
        print(type(packet))
        
        ip_src=packet[IP].src
        ip_dst=packet[IP].dst
        tcp_sport=packet[TCP].sport
        tcp_dport=packet[TCP].dport
        print( " IP src " + str(ip_src) + " TCP sport " + str(tcp_sport))
        print( " IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport))
        payload = packet[TCP].payload #me trying to decode messages
        

        #print("Message: ", udp_payload.decode())
        #print("Packet info:", payload.decode('utf-8', 'ignore'))
        print("Packet info:", payload)
        print("Packet info:", type(payload))
        print("Received packet from port 5000")
        print("Bouncing Info")
        count += 1
        string = "Bouncing: " + str(count)
        packet = IP(dst=ip_src)/TCP(dport=tcp_sport)/ string
        send(packet)


interface = "eth0"  # Change to the interface you want to monitor
sniff(iface=interface, prn=packet_callback, store=0)
