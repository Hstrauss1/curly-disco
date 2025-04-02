from scapy.all import IP, ICMP, sr1

def send_icmp_echo_request(destination_ip):
    # Craft an ICMP echo request packet
    packet = IP(dst=destination_ip) / ICMP(type="echo-request")

    # Send the packet and wait for a response
    response = sr1(packet, timeout=2, verbose=False)

    # Check if a response was received
    if response:
        # If a response was received, print the summary
        response.show()
    else:
        # If no response was received, print a message
        print("No response received.")

# Example usage
if __name__ == "__main__":
    # Change this value to the IP address you want to ping
    destination_ip = "172.16.64.147"
    
    # Send the ICMP echo request
    send_icmp_echo_request(destination_ip)
