import requests
import json

class AI():

    def __init__(self, dev):
        self.dev = dev
        self.tracking_url = 'http://{}:2200/v1/luner'.format(self.dev.ip)
        self.settings_url = 'http://{}:2200/v1/imaging/config'.format(self.dev.ip)

        self.object = [
            "HEAD", "NOSE", "LEFT_EYE", "RIGHT_EYE", "LEFT_EAR", "RIGHT_EAR",
            "UPPER_BODY", "LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_ELBOW", "RIGHT_ELBOW",
            "LEFT_WRIST", "RIGHT_WRIST", "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE", "RIGHT_KNEE", 
            "LEFT_ANKLE", "RIGHT_ANKLE"
        ]

        self.poseDetection = 0 

        self.headers = {'Content-Type':'application/json'}

        self.payload = {
            "trackObject": "LEFT_WRIST",
            "trackInitPolicy": "left",
            "trackLostWaitTime": 20,
            "trackDistThreshold": 0.2,
            "trackPoseThreshold": 0.4,
            "trackPartThreshold": 0.15,
            "trackDrawTracked": 1,
            "state": False,
            "preset": "FOLLOW",
            "hardware": {
                "case": 17,
                "data": {
                "slide": {
                    "points": [],
                    "time": [],
                    "loop": 2,
                    "ramp": 0
                },
                "speeds": {
                    "slide": 0,
                    "pan": 1,
                    "tilt": 1,
                    "transition": 1
                }
                }
            }
        }

    def help(self):
        print("\n---> AI Help <---\n")
        
        print("Function: enable_pose() \nDesciption: Enables pose detection on the Axibo.\n")
        
        print("Function: enable_Tracking() \nDesciption: Enables the tracking on Axibo.\n")
        
        print("Function: set_object() \nDesciption: Sets the object to track.\n")
        
        print("Function: set_InitPolicy() \nDesciption: Sets the left or right target to track.\n")
        
        print("Function: set_slideSpeed() \nDesciption: Sets the slide speed.\n")

        print("Function: set_panSpeed() \nDescription: Sets the pan speed.\n")

        print("Function: set_tiltSpeed() \nDescription: Sets the tilt speed.\n")
        
        print("Function: set_transitionSpeed() \nDescription: Sets the transition speed.\n")

    def enable_pose(self, enable): 
        if self.enable_check(enable) == True:
            url = self.settings_url
            
            payload = json.dumps({ "poseDetection": enable})
            
            ret = requests.put(url, headers = self.headers, data = payload)

            if ret.status_code == 200:
                self.poseDetection = enable
                print("Pose detection set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
    
    def enable_tracking(self, enable):
        url = self.tracking_url
        
        if self.enable_check(enable) == True:
            self.payload["state"] = enable
        
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Tracking set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_object(self, object):
        if self.check_object(object) == True: 
            url = self.tracking_url

            self.payload["trackObject"] = object 

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Tracked object set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))    

    def set_init_policy(self, policy):
        if self.check_policy(policy) == True:
            url = self.tracking_url
            
            self.payload["trackInitPolicy"] = policy

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Target set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_slide_speed(self, speed):
        if self.check_speed(speed) == True: 
            url = self.tracking_url

            self.payload["hardware"]["data"]["speeds"]["slide"] = speed 
            
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Slide speed set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_pan_speed(self, speed):
        if self.check_speed(speed) == True: 
            url = self.tracking_url

            self.payload["hardware"]["data"]["speeds"]["pan"] = speed

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Pan speed set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_tilt_speed(self, speed):
        if self.check_speed(speed) == True: 
            url = self.tracking_url

            self.payload["hardware"]["data"]["speeds"]["tilt"] = speed
            
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Tilt speed set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
    
    def set_transition_speed(self, speed):
        if self.check_speed(speed) == True: 
            url = self.tracking_url

            self.payload["hardware"]["data"]["speeds"]["transition"] = speed
            
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))  

            if ret.status_code == 200:
                print("Transition speed set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def check_state(self, state):
        if state == True or state == False:
            return True
        else:
            raise ValueError("Invalid State.")

    def check_object(self, object):
        for listObject in self.object:
            if listObject == object:
                return True
        raise ValueError("Invalid Object.")

    def check_policy(self, policy):
        if policy == "left" or policy == "right":
            return True
        else:
            raise ValueError("Invalid Policy.")

    def enable_check(self, enable):
        if enable == 0 or enable == 1:
            return True
        else:
            raise ValueError("Invalid Entry.") 

    def check_speed(self, speed):
        if 0 <= speed <= 1:
            return True 
        else:
            raise ValueError("Invalid Speed.")