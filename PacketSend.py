from scapy.all import IP,TCP,Ether,sendp,send,Raw
import time
import random
#open terminal and run both programs at the same time
#to execute use:
#sudo pipx run --spec scapy python3 ___.py
#
def encode_message(message):
    # Define the mapping for each letter
    encoding_map = {
        'a': '1s', 'b': '5g', 'c': '9z', 'd': '3k', 'e': '7b', 'f': '8m',
        'g': '0x', 'h': 'b3', 'i': '2l', 'j': '4f', 'k': '6d', 'l': 'q1',
        'm': 'w5', 'n': 'e9', 'o': 'r7', 'p': 't3', 'q': 'y0', 'r': 'u2',
        's': 'i8', 't': 'o4', 'u': 'p6', 'v': 'a1', 'w': 's5', 'x': 'd0',
        'y': 'f2', 'z': 'h4', ' ' : 'masfq'
    }
    encoded_message = ""
    
    # Process each character in the message
    for char in message.lower():
        if char in encoding_map:
            encoded_message += encoding_map[char]
        else:
            encoded_message += char  
    return encoded_message

def chop_message(message, length):
    chopped_list = []
    for i in range(0, len(message), length):
        chopped_list.append(message[i:i + length])
    return chopped_list


def test(num, val):
    string=input("input password:\n")
    dst1="172.16.64.147"
    #string = "password"
    packet = IP(dst=dst1)/TCP(dport=num)/ string
    send(packet)
    messg=input("input message:\n")
    messg=encode_message(messg)
    length = len(messg)
    if length>20:
        length = 10
    else:
        length = 2
    chopped_mssg = chop_message(messg, length)
    j=0
    for part in chopped_mssg:
        j+=1
        packet2 = IP(dst=dst1)/TCP(dport=num)/ part
        send(packet2)
        time.sleep(.3)
        print("Sending section: ", j)






if __name__ == "__main__":
    destination_interface = "en0"  
    destination_ip = "172.16.64.147"  
    destination_mac = "dc:a6:32:c5:b3:d7" 
    destination_port = 5000 
    number = 0
    for _ in range(1):
        number += 1
        #print(number)
        #random_number = random.randint(4950, 5050)
        test(5000, number)
        
