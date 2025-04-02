from scapy.all import sniff, TCP, IP
count = 0

def packet_callback(packet):
    global count
    if packet.haslayer('TCP') and packet[TCP].sport == 5000:
        count+=1
        print("Received bounce from port 5000")
        if count==10:
            exit(1)

interface = "en0"  
sniff(iface=interface, prn=packet_callback, store=0)
