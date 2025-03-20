import subprocess
import unittest

def grab_ip():
    hostname_cmd = (['hostname', '-I'])
    result = subprocess.run(hostname_cmd, capture_output=True, text=True)
    out = result.stdout.strip()
    print(out)
    print()
    
    return out

def add_ip():
    ip = grab_ip()
    if ("172.24.156.196" in ip) and ("192.168.1.101" not in ip):
        add_ip_cmd = (['sudo', 'ip', 'addr', 'add', '192.168.1.101/24', 'dev', 'eth0'])
        result = subprocess.run(add_ip_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        return True
        
    elif ("172.24.156.196" in ip) and ("192.168.1.102" not in ip):
        add_ip_cmd = (['sudo', 'ip', 'addr', 'add', '192.168.1.102/24', 'dev', 'eth0'])
        result = subprocess.run(add_ip_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        return True
    
    elif ("192.168.1.102" in ip) or ("192.168.1.101" in ip):
        print ("Ip already added.")
        return True
    
    else:
        return False
    
def ping_pi():
    ip = grab_ip()
    if ("192.168.1.101" in ip):
        ping_cmd = (['ping', '-c', '4', '192.168.1.102'])  # Ping 4 times
        result = subprocess.run(ping_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        return "0% packet loss" in out  # Check if ping was successful
    elif("192.168.1.102" in ip):
        ping_cmd = (['ping', '-c', '4', '192.168.1.101'])  # Ping 4 times
        result = subprocess.run(ping_cmd, capture_output=True, text=True)
        out = result.stdout
        print(out)
        return "0% packet loss" in out  # Check if ping was successful

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
