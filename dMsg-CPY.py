import subprocess

def filter_dmesg_for_packets():
    try:
        #print("hi3")
        dmesg_output = subprocess.check_output(["dmesg"]).decode("utf-8")
        filtered_messages = []
        
        for line in dmesg_output.split('\n'):
            if "Intercepted packet" in line:
                print("hi2")
                message_start_index = line.find("Intercepted packet") + len("Intercepted packet")
                message = line[message_start_index:].strip()
                filtered_messages.append(message)
        #print("hi")
        return filtered_messages
    except subprocess.CalledProcessError:
        return ["Error: Failed to execute dmesg command"]

while True:
    filtered_messages = filter_dmesg_for_packets()
    for message in filtered_messages:
        print(message)