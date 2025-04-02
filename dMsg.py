import subprocess

def filter_dmesg_for_packets():
    try:
        dmesg_output = subprocess.check_output(["dmesg"]).decode("utf-8")
        filtered_lines = [line for line in dmesg_output.split('\n') if any(keyword in line.lower() for keyword in ["tcp","Message"])]
        filtered_output = '\n'.join(filtered_lines)
        
        return filtered_output
    except subprocess.CalledProcessError:
        return "Error: Failed to execute dmesg command"
    
filtered_output = filter_dmesg_for_packets()
print(filtered_output)
