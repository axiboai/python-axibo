import requests
import json 

class System():

    def __init__(self, dev):
        self.dev = dev

        self.system_status_url = 'http://{}:2200/v1/system/status'.format(self.dev.ip)
        self.system_bluetooth_url = 'http://{}:2200/v1/system/bluetooth'.format(self.dev.ip)
        self.system_bluetooth_configure_url = 'http://{}:2200/v1/system/bluetooth-config'.format(self.dev.ip)
        self.system_wifi_url = 'http://{}:2200/v1/system/wifiInfo'.format(self.dev.ip)
        self.system_redis_url = 'http://{}:2200/v1/system/redis-params'.format(self.dev.ip)
        self.system_get_wifi_url = 'http://{}:2200/v1/system/wifi'.format(self.dev.ip)
        self.system_update_url = 'http://{}:2200/v1/system/update'.format(self.dev.ip)
        self.system_services_url = 'http://{}:2200/v1/system/services'.format(self.dev.ip)
        self.system_info_url = 'http://{}:2200/v1/system/info'.format(self.dev.ip)
        self.system_web_url = 'http://{}:2200/v1/websocket/Info'.format(self.dev.ip)

        self.system_config_url = 'http://{}:2200/v1/system/config'.format(self.dev.ip)
        self.system_reboot_url = 'http://{}:2200/v1/system/reboot'.format(self.dev.ip)

    def help(self):
        print("\n---> System Help <---\n")
        
        print("Function: get_system_status() \nDesciption: Returns system status.\n")
        
        print("Function: get_bluetooth_status() \nDesciption: Returns bluetooth devices status.\n")
        
        print("Function: get_wifi_status() \nDesciption: Returns wifi status.\n")
        
        print("Function: get_redis_sarams() \nDesciption: Returns redis parameters.\n")
        
        print("Function: get_wifi_list() \nDesciption: Lists the current wifi.\n")

        print("Function: get_update() \nDescription: Returns update status.\n")

        print("Function: get_system_services() \nDesciption: Returns which system services are currently active.\n")
        
        print("Function: get_system_info() \nDesciption: Returns general system information.\n")

        print("Function: get_websockets() \nDescription: Returns the websocket routes.\n")

        print("Function: configure_bluetooth() \nDesciption: Scan, delete, and connect to blutooth.\n")
        
        print("Function: connect_wifi() \nDesciption: Connect to wifi (requires power cycle).\n")

        print("Function: delete_wifi() \nDescription: Deletes wifi networks.\n")

        print("Function: start_stop() \nDescription: Start and stop system services.\n")

        print("Function: reboot() \nDescription: Reboots Axibo.\n")

    def get_system_status(self):
        url = self.system_status_url

        ret = requests.get(url)

        if ret.status_code == 200:
            self.print_json(ret.content)        
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_bluetooth_status(self):
        url = self.system_bluetooth_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
            return json.loads(ret.content)
        else:
            raise ValueError("Received unexpected status code {]".format(ret.status_code))

    def get_wifi_status(self):
        url = self.system_wifi_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_redis_params(self):
        url = self.system_redis_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_wifi_list(self):
        url = self.system_get_wifi_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
            return json.loads(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_update(self):
        url = self.system_update_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_system_services(self):
        url = self.system_services_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
            return json.loads(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_system_info(self):
        url = self.system_info_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))
    
    def get_websockets(self):
        url = self.system_web_url

        ret = requests.get(url)

        if ret.status_code == 200: 
            self.print_json(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    #1 - scan, 2 - delete, 3 - connect
    def configure_bluetooth(self, case, mac):
        url = self.system_bluetooth_configure_url

        if case == 1 or case == 2 or case == 3:

            payload = json.dumps({
                "case": case,
                "mac": mac
            })
            
            headers = {'Content-Type': 'application/json'}

            ret = requests.put(url, headers = headers, data = payload)
            self.print_json(ret.content)

            if case == 1:
                print("Scanning Bluetooth Devices...")
            elif case == 2: 
                print("Deleting Bluetooth Device...")
            elif case == 3:
                print("Connecting Bluetooth Device...")

            return json.loads(ret.content)
            
    def connect_wifi(self, ssid, password):
        url = self.system_get_wifi_url

        payload = json.dumps({
            "ssid": "axibo-50gs",
            "password": "onebillion"
        })
        headers = {'Content-Type': 'application/json'}

        ret = requests.put(url, headers = headers, data = payload)

        self.print_json(ret.content)
        
    def delete_wifi(self, ssid):
        url = self.system_get_wifi_url

        payload = json.dumps({
            "ssid": "axibo-50gs"
        })
        headers = {'Content-Type': 'application/json'}

        ret = requests.delete(url, headers = headers, data = payload)

        self.print_json(ret.content)

    def start_stop(self, camera = 0, hardware = 0, tracker = 0, hdmiManager = 0):
        url = self.system_config_url
        
        payload = json.dumps({
            "camera": camera,
            "hardware": hardware,
            "tio": tracker,
            "hdmiManager": hdmiManager
        })
        headers = {'Content-Type': 'application/json'}

        ret = requests.put(url, headers = headers, data = payload)

        self.print_json(ret.content)

    def reboot(self):
        url = self.system_reboot_url

        ret = requests.post(url)

        if ret.status_code == 200:
            self.print_json(ret.content)
            print("Rebooting...")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def print_json(self, content):
        obj = json.loads(content)
        
        json_formatted_str = json.dumps(obj, indent = 4)

        print(json_formatted_str)