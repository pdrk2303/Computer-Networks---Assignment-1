

import subprocess
import re


def extract_ip(line):
    match = re.search(r"\d+\.\d+\.\d+\.\d+", line)
    if match:
        return match.group()
    return None

def extract_rtt(line):
    match = re.search(r"Max rtt: (\d+\.\d+)ms", line)
    if match:
        return match.group(1)
    return None

def extract_dest_ip(line):
    match = re.search(r"ICMP \[.+ > (.+) Echo request", line)
    if match:
        return match.group(1)
    return None
        

def traceroute(destination, max_hops=30):
    print(f"Tracing route to {destination} over a maximum of {max_hops} hops:")
    for ttl in range(1, max_hops + 1):
        cmd = f"nping -c 1 --ttl {ttl} {destination}"
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            lines = result.stdout.split("\n")
            dest_ip = extract_dest_ip(lines[2])
            #print(lines, len(lines))
            flag = False
            for line in lines:
                if "RCVD" in line and "TTL=0 during transit" in line:
                    flag = True
                    hop_ip = extract_ip(line)
                    rtt = extract_rtt(lines[5])
                    if rtt:
                        print(f"{ttl} {rtt}ms {hop_ip}")
                    else:
                        #print(result.stdout)
                        print(f"{ttl} * {hop_ip}")
                        
                    break
                elif "RCVD" in line and "Echo reply" in line:
                    flag = True
                    hop_ip = extract_ip(line)
                    rtt = extract_rtt(lines[5])
                    if rtt:
                        print(f"{ttl} {rtt}ms {hop_ip}")
                    else:
                        #print(result.stdout)
                        print(f"{ttl} * {hop_ip}")
                        
                    if hop_ip == dest_ip:
                        print("Trace Complete.")
                        return
                    break
                
                
            if not flag:
                print(f"{ttl} * Request timed out.")
            

        except subprocess.CalledProcessError:
            print(f"{ttl}: Error executing nping command")
            

target_host = "www.google.com"
traceroute(target_host)














