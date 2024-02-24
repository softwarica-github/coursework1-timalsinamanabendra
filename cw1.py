import socket
import concurrent.futures

# A dictionary mapping common port numbers to services
COMMON_SERVICES = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    443: 'HTTPS',
    3306: 'MySQL',
    8080: 'HTTP-Proxy'
}

# Simplistic OS detection based on common services
def guess_os_by_service(services):
    if 'SSH' in services:
        return 'Likely Unix/Linux based'
    if 'SMTP' in services or 'HTTP-Proxy' in services:
        return 'Could be any OS'
    if 'Telnet' in services:
        return 'Possibly an older or embedded system'
    return 'OS detection not conclusive based on services'

def check_port(host, port, services_detected):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Set a timeout for the connection attempt
        result = s.connect_ex((host, port))
        if result == 0:
            service = COMMON_SERVICES.get(port, 'Unknown')
            print(f"Port {port} is open (Service: {service})")
            if service != 'Unknown':
                services_detected.add(service)

if __name__ == "__main__":
    host = socket.gethostbyname(input("Enter the domain: "))
    services_detected = set()
    a = 0
    b = 65535
    max_workers = 65535
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_port, host, port, services_detected) for port in range(a, b+1)]
        concurrent.futures.wait(futures)
    
    os_guess = guess_os_by_service(services_detected)
    print(f"Based on detected services, {os_guess}")