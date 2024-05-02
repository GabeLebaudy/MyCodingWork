#This file will be for connecting to the VPN, ensuring the IP is switched, for avoiding IP bans

#Imports
import subprocess, requests, time, sched, socket, random

#IP Class
class DynamicIP:
    #Constructor
    def __init__(self):
        self.current_ip = None
        self.my_ip = None
        self.current_area = None

    #Getters
    def getMyIP(self):
        return self.my_ip
    
    def getProxyIP(self):
        return self.current_ip

    #Verify My IP Address
    def verifyMyIP(self):
        #There a few possiblilities for how this could work. Since nordvpn commands don't return much info, I have to verify them another way.
        temp_ip = self.getPublicIP()
        if not self.disconnect():
            #There was an error with the VPN, kill the program
            return False

        new_ip = self.getPublicIP()
        if temp_ip != new_ip:
            #If the IP's are different, the disconnect was successful, which means new_ip is my IP
            self.my_ip = new_ip
            didConnect = self.connectToRandomArea()
            if not didConnect:
                return False
        
            return True
        else:
            #Either the VPN was disconnected from the start, or the VPN commands do not work.
            didConnect = self.connectToRandomArea()
            if not didConnect:
                #Error message with the VPN, abort program
                return False
            
            if self.current_ip == new_ip:
                #VPN Commands are not working abort the program
                return False
            else:
                self.my_ip = new_ip
                return True

    #Get the current public IP
    def getPublicIP(self):
        try:
            url = 'https://httpbin.org/ip'
            response = requests.get(url)
            ip = response.json()['origin']
            return ip
        except:
            #When VPN is connecting, requests to websites will cause an error.
            return False
    
    #Disconnect from NordVPN
    def disconnect(self):
        command = ["C:\\Program Files\\NordVPN\\nordvpn", "--disconnect"]
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = sub.communicate()

        #If the error message contains any text, kill the program
        if error.decode("ascii"):
            return False
        return True
    
    #Connect to random area that works with the website
    def connectToRandomArea(self):
        prior_ip = self.getPublicIP()

        potential_areas = ["new york", "manassas", "buffalo", "charlotte", "atlanta", "miami", "dallas", "saint louis", "chicago", "kansas city", "denver", "salt lake city", "phoenix", "los angeles", "san francisco", "seattle"]
        new_area = random.choice(potential_areas)
        while new_area == self.current_area:
            new_area = random.choice(potential_areas)

        command = ["C:\\Program Files\\NordVPN\\nordvpn", "-c", "-g", new_area]
        sub = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = sub.communicate()
        if error.decode("ascii"):
            return False

        #Ensure VPN is properly connected before proceeding
        count = 0
        new_ip = self.getPublicIP()
        while (prior_ip == new_ip) or (not new_ip) or (new_ip == self.my_ip):
            count += 1
            if count > 14:
                return False
            
            new_ip = self.getPublicIP()
            time.sleep(2)
            
        self.current_ip = new_ip
        self.current_area = new_area
        return True

#Main Method for testing
if __name__ == "__main__":
    test_case = DynamicIP()
    test_case.verifyMyIP()