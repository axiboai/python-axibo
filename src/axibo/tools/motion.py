from re import A
import requests
import json
import time

class MotionRoute():

    def __init__(self, dev):
        self.dev = dev
        self.motion_config_url = 'http://{}:2200/v1/direct-control/config'.format(self.dev.ip)
        self.motion_homing_url = 'http://{}:2200/v1/direct-control/home'.format(self.dev.ip)
        self.motion_switch_url = 'http://{}:2200/v1/direct-control/switch-mode'.format(self.dev.ip)
        self.motion_focus_url = 'http://{}:2200/v1/direct-control/focus'.format(self.dev.ip)
        self.motion_packet_url = 'http://{}:2200/v1/direct-control/packet-confirmation'.format(self.dev.ip)
        self.motion_move_abso_url = 'http://{}:2200/v1/direct-control/move-absolute'.format(self.dev.ip)
        self.motion_move_rel_url = 'http://{}:2200/v1/direct-control/move-relative'.format(self.dev.ip)
        self.motion_status_url = 'http://{}:2200/v1/direct-control/motion-status'.format(self.dev.ip)
        self.motion_config_hardware_url = 'http://{}:2200/v1/direct-control/hardware-config'.format(self.dev.ip)
        self.motion_trigger_url = 'http://{}:2200/v1/direct-control/trigger'.format(self.dev.ip)
        self.motion_stop_url = 'http://{}:2200/v1/direct-control/stop-motion'.format(self.dev.ip)

        self.headers = {'Content-Type':'application/json'}

        self.payload_motion = {
                "tilt": {
                    "accel": 1,
                    "current": 12,
                    "maxPos": 45,
                    "maxVel": 25,
                    "minPos": -45,
                    "speed": 15,
                },
                "pan": {
                    "accel": 1,
                    "current": 12,
                    "maxPos": 180,
                    "maxVel": 25,
                    "minPos": -180,
                    "speed": 15,
                },   
                "slide": {
                    "accel": 1,
                    "current": 12,
                    "maxPos": 500,
                    "maxVel": 25,
                    "minPos": 0,
                    "speed": 10,
                }
                # "focus": {
                #     "accel": 1,
                #     "current": 12,
                #     "maxPos": 360,
                #     "maxVel": 25,
                #     "minPos": 360,
                #     "speed": 10,
                # },
                # "zoom": {
                #     "accel": 1,
                #     "current": 12,
                #     "maxPos": 360,
                #     "maxVel": 25,
                #     "minPos": -360,
                #     "speed": 10,
                # }                  
        }

        self.payload_homing = {
            "pan": { 
                "direction": 0,
                "homingSpeed": 40,
                "maxPos": 10,
                "minPos": -10,
                "useTorque": 0
            },
            "tilt": {
                "direction": 0,
                "homingSpeed": 40,
                "maxPos": 10,
                "minPos": -10,
                "useTorque": 0
            }, 
            "slide": {
                "direction": 0,
                "homingSpeed": 10
            },
            "focus": {
                "direction": 0,
                "homingSpeed": 40,
                "maxPos": 10,
                "minPos": -10,
                "useTorque": 0
            },
            "zoom": {
                "direction": 0,
                "homingSpeed": 40,
                "maxPos": 10,
                "minPos": -10,
                "useTorque": 0
            }
        }
        
        self.payload_trigger = {
            "trigCase": 0,
            "timeSpacing": 5000,
            "pauseAmount": 5000,
            "count": 10,
            "bulb": 0.1,
            "focus": 0
        }

        self.payload_absolute = {
                "pan": [
                    0,
                    0
                ],
                "tilt": [
                    0,
                    0
                ],
                "slide": [
                    0, 
                    0
                ]
                # "focus": [
                #     0,
                #     0
                # ],
                # "zoom": [
                #     0,
                #     0
                # ]
        }

        self.payload_relative = {
                "pan": [
                    0,
                    0
                ],
                "tilt": [
                    0,
                    0
                ],
                "slide": [
                    0, 
                    0
                ]
                # "focus": [
                #     0,
                #     0
                # ],
                # "zoom": [
                #     0,
                #     0
                # ]
        }

    # def help():
    #     print("\n---> Motion Help <---\n")
        
    #     print("Function: configure_motion() \nDesciption: Configure the Axibos motion parameters for a specific axis.\n")
        
    #     print("Function: configure_motion_all() \nDesciption: Configure the Axibos motion parameters for all axis.\n")
        
    #     print("Function: configure_homing() \nDesciption: Configure homing for a single axis.\n")
        
    #     print("Function: configure_homing_all() \nDesciption: Configure homing for all axis.\n")
        
    #     print("Function: switch_modes() \nDesciption: Switch between highspeed and hightorque.\n")

    #     print("Function: packet_conf() \nDescription: Set the packet configuration.\n")

    #     print("Funciton: set_absolute_move() \nDescription: Set the position and speed of the next absolute move.\n")

    #     print("Funciton: set_relative_move() \nDescription: Set the position and speed of the next relative move.\n")

    #     print("Function: move_set_axies() \nDescription: Perform the next set of moves.\n")

    #     print("Function: move_json() \nDescription: Insert json format and move axies.\n")

    #     print("Function: trigger_control() \nDescription: Configure the trigger control.\n")

    #     print("Function: stop_motion() \nDescription: Stops all Axibo motion.\n")

    #     print("Function: get_motion_status() \nDescription: Returns the motion status.\n")

    #     print("Function: get_config_hardware() \nDescription: Returns the hardware configuration.\n")
    
    def get_connected_motors(self):
        print(self.dev.stream.connected_axis)

    def configure_motor(self, axis, accel = 1, current = 12, maxPos = 150, minPos = -150, maxVel = 40, speed = 10):
        url = self.motion_config_url

        if 1 > current > 16: 
            raise ValueError("Invalid current.")

        if self.check_axis(axis) == True:
            
            self.payload_motion[axis]["accel"] = accel
            self.payload_motion[axis]["current"] = current
            self.payload_motion[axis]["maxPos"] = maxPos
            self.payload_motion[axis]["minPos"] = minPos
            self.payload_motion[axis]["maxVel"] = maxVel
            self.payload_motion[axis]["speed"] = speed

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload_motion))

            if ret.status_code == 200:
                print("Motion configure successful.")
                return ret.content
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def configure_motor_json(self, json_format):
        url = self.motion_config_url

        ret = requests.put(url, headers = self.headers, data = json.dumps(json_format))

        if ret.status_code == 200:
            print("Motion configure successful.")
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def calibrate_motor(self, axis, speed = 40, maxPos = 10, minPos = -10):
        url = self.motion_homing_url
        payload={axis:{}}
        if self.check_axis_homing(axis) == True:
            
            payload[axis]["homingSpeed"] = speed
            payload[axis]["maxPos"] = maxPos
            payload[axis]["minPos"] = minPos
            # self.payload[axis]["useTorque"] = useTorq

            ret = requests.put(url, headers = self.headers, data = json.dumps(payload))

        if ret.status_code == 200:
            print("Homing successful.")
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def calibrate_motor_json(self, json_format):
        url = self.motion_homing_url

        ret = requests.put(url, headers = self.headers, data = json.dumps(json_format))

        if ret.status_code == 200:
            print("Homing successful.")
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def switch_mode(self, mode):
        url = self.motion_switch_url

        if mode == "highspeed" or mode == "hightorque":
            mode = mode
        else:
            raise ValueError("Invalid Mode.")

        payload = json.dumps({"mode": mode})

        ret = requests.put(url, headers = self.headers, data = payload)

        if ret.status_code == 200:
            print("Axibo mode switch successful.")
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    # def focus_calib(self, case = 1, name = "", maxDeg = 180):
    #     url = self.motion_focus_url

    #     payload = json.dumps({
    #         "case": case, 
    #         "name":name,
    #         "maxdeg":maxDeg
    #     })

    #     ret = requests.put(url, headers = self.headers, data = payload)

    #     self.print_json(ret.content)

    def packet_conf(self, mode):
        url = self.motion_packet_url

        if  mode == 1 or mode == 0:
            mode = mode
        else:
            raise ValueError("Invalid Packet Configuration.")

        payload = json.dumps({"mode": mode,})

        ret = requests.put(url, headers = self.headers, data = payload)

        if ret.status_code == 200:
            print("Axibo packet configure successful.")
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_absolute_move(self, axis, pos=0, speed=0):
        self.type="absolute"
        if self.check_axis(axis) == True:
            self.payload_absolute[axis][0] = pos
            self.payload_absolute[axis][1] = speed 

            print("Absolute payload set successful.") 

    def set_relative_move(self, axis, pos=0, speed=0):
        self.type="relative"
        if self.check_axis(axis) == True:    
            self.payload_relative[axis][0] = pos
            self.payload_relative[axis][1] = speed

            print("Absolute payload set successful.") 

    def move_now(self):
        if self.type == "absolute":
            url = self.motion_move_abso_url

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload_absolute))

            for axis in ["tilt", "pan", "slide"]: #"focus", "zoom"]:
                self.payload_absolute[axis][0] = 0
                self.payload_absolute[axis][1] = 0

            if ret.status_code == 200:
                print("Move successful.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
        elif self.type == "relative":
            url = self.motion_move_rel_url

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload_relative))

            self.payload_relative = {"tilt":[0,0],"pan":[0,0],"slide":[0,0]}
            
            if ret.status_code == 200:
                print("Move successful.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
        else:
            print("Enter valid type.")

    def move_json(self, type, json_format):
        if type == "relative":
            url = self.motion_move_rel_url

            ret = requests.put(url, headers = self.headers, data = json.dumps(json_format))

            if ret.status_code == 200:
                print("Move successful.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
        elif type == "absolute":
            url = self.motion_move_abso_url

            ret = requests.put(url, headers = self.headers, data = json.dumps(json_format))

            if ret.status_code == 200:
                print("Move successful.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
        else:
            print("Enter valid type.")

    def trigger_control(self, trigCase=0, timeSpacing=5000, pauseAmount=5000, count=10, bulb=0.1, focus=0):
        url = self.motion_trigger_url

        self.payload_trigger["trigCase"] = trigCase
        self.payload_trigger["timeSpacing"] = timeSpacing
        self.payload_trigger["pauseAmount"] = pauseAmount
        self.payload_trigger["count"] = count
        self.payload_trigger["bulb"] = bulb
        self.payload_trigger["focus"] = focus

        ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))

        if ret.status_code == 200:
            print("Trigger control set successfully.")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def stop(self):
        url = self.motion_stop_url

        headers = {}
        payload = {}

        ret = requests.put(url, headers = headers, data = payload)
        
        if ret.status_code == 200:
            print("All motion Stopped.")
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code)) 

    def get_motion_status(self):
        url = self.motion_status_url

        ret = requests.get(url)

        if ret.status_code == 200:
            self.print_json(ret.content)
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    #This function will wait for the move to be completed.
    def move_wait(self):
        time.sleep(0.5)
        flag=1
        while True: 
            for device in self.dev.stream.connected_axis:
                # print(device)
                flag=self.dev.stream.device_status_message[device]["isBusy"]

            if flag==0:
                print("Move Complete.")
                # self.get_location()
                break
            time.sleep(0.1)

    #Gets the current location.
    def get_location(self):
        list=[]
        for device in self.dev.stream.connected_axis:
            print("{} : {}".format(device,str(self.dev.stream.device_status_message[device]["position"])))
            list.append(self.dev.stream.device_status_message[device]["position"])
        return list
        # tiltLoc = self.dev.stream.device_status_message["tilt"]["position"]
        # panLoc = self.dev.stream.device_status_message["pan"]["position"]
        # slideLoc = self.dev.stream.device_status_message["slide"]["position"]
        # focusLoc = self.dev.stream.device_status_message["focus"]["position"]
        # zoomLoc = self.dev.stream.device_status_message["zoom"]["position"]

    def get_configHardware(self):
        url = self.motion_config_hardware_url

        ret = requests.get(url)
        
        if ret.status_code == 200:
            self.print_json(ret.content)
            return ret.content
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def check_axis(self, axis):
        
        if axis == "tilt" or axis == "pan" or axis == "slide" or axis == "focus" or axis == "zoom":
            return True
        else:
            raise ValueError("Invalid Axis.")

    def check_axis_homing(self, axis):
        if axis == "tilt" or axis == "pan" or axis == "slide" or axis == "focus" or axis == "zoom":
            return True
        else:
            raise ValueError("Invalid Axis.")

    def print_json(self, content):
        obj = json.loads(content)
        
        json_formatted_str = json.dumps(obj, indent = 4)

        print(json_formatted_str)
    
    def stream_move_json(self, type, json_format):
        if type == "relative":
            command = {
                "name": "fromClient",
                "data":
                {
                    "case": "controlCMDRel",
                    "moveData": 
                        json_format
                    
                }
            }
            self.dev.stream.ws.send(json.dumps(command))
            
        elif type == "absolute":
            command = {
                "name": "fromClient",
                "data":
                {
                    "case": "controlCMDAbs",
                    "moveData": 
                        json_format
                }
            }
            self.dev.stream.ws.send(json.dumps(command))
        else:
            print("Enter valid type.")
