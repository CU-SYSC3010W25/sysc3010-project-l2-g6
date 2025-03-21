import subprocess
import unittest

def grab_ip():
    # Use `ipconfig` to get the IP address on Windows
    ipconfig_cmd = ['ipconfig']
    result = subprocess.run(ipconfig_cmd, capture_output=True, text=True)
    out = result.stdout

    # Extract IPv4 addresses from the output
    ip_addresses = []
    for line in out.splitlines():
        if "IPv4 Address" in line:
            ip = line.split(":")[1].strip()
            ip_addresses.append(ip)
    
    print("Detected IPs:", ip_addresses)
    return ip_addresses

def add_ip():
    ips = grab_ip()
    if ("172.17.142.144" in ips) and ("192.168.1.101" not in ips):
        # Add IP address using `netsh` on Windows
        add_ip_cmd = ['netsh', 'interface', 'ip', 'add', 'address', 'name="Ethernet"', 'addr=192.168.1.101', 'mask=255.255.255.0']
        result = subprocess.run(add_ip_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        return True
        
    elif ("172.31.32.1" in ips):
        # Add IP address using `netsh` on Windows
        add_ip_cmd = ['netsh', 'interface', 'ip', 'add', 'address', 'name="Ethernet"', 'addr=192.168.1.102', 'mask=255.255.255.0']
        result = subprocess.run(add_ip_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        return True
    
    elif ("192.168.1.102" in ips) or ("192.168.1.101" in ips):
        print("IP already added.")
        return True
    
    else:
        return False

def ping_pi():
    ips = grab_ip()
    if "192.168.1.101" in ips:
        # Ping the other device 4 times
        ping_cmd = ['ping', '-n', '4', '192.168.1.102']  # Windows uses `-n` instead of `-c`
        result = subprocess.run(ping_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        if "unreachable" in out.lower() or "timed out" in out.lower():
            return False
        return True  # Check if ping was successful
    elif "192.168.1.102" in ips:
        # Ping the other device 4 times
        ping_cmd = ['ping', '-n', '4', '192.168.1.101']  # Windows uses `-n` instead of `-c`
        result = subprocess.run(ping_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        if "unreachable" in out.lower() or "timed out" in out.lower():
            return False
        return True  # Check if ping was successful

    return False

class TestEthernet(unittest.TestCase):
    def test_add_ip(self):
        result = add_ip()
        self.assertTrue(result)
            
    def test_ping_pi(self):
        result = ping_pi()
        self.assertTrue(result)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestEthernet('test_add_ip'))
    suite.addTest(TestEthernet('test_ping_pi'))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)