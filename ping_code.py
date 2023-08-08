

import subprocess

def traceroute(destination, max_hops):
    
    for ttl in range(1, max_hops + 1):
        try:
            ping_command = ['ping', '-n', '3', '-i', str(ttl), destination]
            result = subprocess.run(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            
            if "Reply from" in output:
                IPaddr = output.split()[2][1:-1]
                time1 = output.split()[11][5:] if not output.split()[11:15] == ["TTL", "expired", "in", "transit."] else "*"
                time2 = output.split()[15][5:] if not output.split()[18:22] == ["TTL", "expired", "in", "transit."] else "*"
                time3 = output.split()[19][5:] if not output.split()[25:29] == ["TTL", "expired", "in", "transit."] else "*"
                print(f"{ttl} {time1} {time2} {time3} {IPaddr}")
                
            if "Destination host unreachable" in output:
                print(f"{ttl}: {destination}")
            
                
        except:
            print("ERROR")
            
    print("Trace Complete.")
            
traceroute("www.iitd.ac.in", 15)







