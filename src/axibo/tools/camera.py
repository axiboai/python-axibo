from re import L
from io import BytesIO
import requests
import numpy as np

import json

class Camera():

    def __init__(self, dev):
        self.dev = dev
        self.settings_url = 'http://{}:2200/v1/imaging/config'.format(self.dev.ip)
        self.imgCalibration_url = 'http://{}:2200/v1/imaging/calib'.format(self.dev.ip)
        self.stream_url ='http://{}:2101/mjpeg'.format(self.dev.ip)
        self.opencv_flag=False
        self.pil_flag=False
        self.headers = {'Content-Type':'application/json'}
        
        self.payload = {
            'case': 2,
            'feed': '00',
            'imgWidth': 640,
            'imgheight': 480,
            'rotation': '0',
            'exposure': 0.03,
            'autoExpo': 0,
            'hdmiRotation': '0'
        }
         
        #Valid Axibo Resolution Sizes.
        self.valid_resolution = { 
            640 : 480,
            720 : 576,
            960 : 640,
            1024 : [512, 768],
            1920 : 1080
        }

    # def help(self):
    #     print("\n---> Camera Help <---\n")
        
    #     print("Function: capture_image_to_file() \nDesciption: Captures the Axibo camera feed to an external file.\n")
        
    #     print("Function: capture_pil_image() \nDesciption: Captures the PIL image.\n")
        
    #     print("Function: camera_view() \nDesciption: Starts the Axibo live camera feed.\n")
        
    #     print("Function: set_camera() \nDesciption: Sets the camera settings.\n")

    #     print("Function: set_case() \nDescription: Whether the feed is from the Axibo or a HDMI camera.\n")

    #     print("Function: set_resolution() \nDescription: Sets the Axibo and HDMI resolution.\n")
        
    #     print("Function: set_rotation() \nDescription: Sets the rotation of the Axibo camera feed.\n")

    #     print("Function: set_hdmiRotation() \nDescription: Sets the rotation of the HDMI camera feed.\n")

    #     print("Function: set_feed() \nDescription: Sets whether the Axibo or HDMI feed is bigger.\n")

    #     print("Function: set_exposure() \nDescription: Sets the exposure of the Axibo camera.\n")

    #     print("Function: enable_autoExposure() \nDescription: Enables auto exposure.\n")

    #     print("Function: get_config() \nDescription: Returns the camera settings.\n")

    #     print("Function: get_calibrationMatrix() \nDescription: Returns the calibration matrix.\n")

    def capture_image_to_file(self, file_name='axibo_image.jpg'):
        response = self.request_get_image()
        with open(file_name, 'wb') as f:
            f.write(response.content)

    def capture_pil_image(self):
        if not self.pil_flag:
            from PIL import Image
        response = self.request_get_image()
        return Image.open(BytesIO(response.content))
    
    def request_get_image(self):
        url = "http://{}:2200/v1/".format(self.dev.ip) + "imaging/cam"
        ret = requests.get(url)
        return ret
    
    def camera_view(self):
        if not self.opencv_flag:
            import cv2
        r = requests.get(self.stream_url, stream=True)
        if(r.status_code == 200):
            bytes = b""
            for chunk in r.iter_content(chunk_size=1024):
                bytes += chunk
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes = bytes[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    cv2.imshow('Axibo Live Feed: Press ESC to Close', i)
                    if cv2.waitKey(1) == 27: # ESC key 
                        exit(0)

    def set_camera(self, case=2, feed='00', imgWidth=640, imgHeight=480, rotation='0', exposure=0.03, autoExpo=0, hdmiRotation='0'): 
        
        checks = [
            self.check_case(case), 
            self.check_feed(feed),
            self.check_resolution(imgWidth, imgHeight),
            self.check_image_rotation(rotation), 
            self.check_exposure(exposure), 
            self.enable_check(autoExpo),
            self.check_hdmi_rotation(hdmiRotation)
        ]

        if all(checks):
            url = self.settings_url
            
            self.payload['case'] = case
            self.payload['feed'] = feed
            self.payload['imgWidth'] = imgWidth
            self.payload['imgheight'] = imgHeight
            self.payload['rotation'] = rotation
            self.payload['exposure'] = exposure
            self.payload['autoExpo'] = autoExpo
            self.payload['hdmiRotation'] = hdmiRotation
            
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))

            if ret.status_code == 200:
                print("Camera settings set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_case(self, case):
        if self.check_case(case):
            url = self.settings_url

            self.payload["case"] = case

            ret = requests.put(url, headers = self.headers , data = json.dumps(self.payload))

            if ret.status_code == 200:
                return print("Case set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_resolution(self, width, height):

        if self.check_resolution(width, height) == True:
            url = self.settings_url 
            
            self.payload["imgWidth"] = width
            self.payload["imgheight"] = height   

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload)) 

            if ret.status_code == 200:
                print("Image width and height set successfully.")
            else: 
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_rotation(self, rotation):
        if self.check_image_rotation(rotation) == True:
            url = self.settings_url
           
            self.payload["rotation"] = rotation

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))

            if ret.status_code == 200:
                print("Axibo rotation set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))
             
    def set_hdmi_rotation(self, rotation):
        if self.check_image_rotation(rotation) == True:
            url = self.settings_url

            self.payload["hdmiRotation"] = rotation
            
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))

            if ret.status_code == 200:
                print("HDMI rotation set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_feed(self, feed):
        if self.check_feed(feed) == True:
            url = self.settings_url
            
            self.payload["feed"] = feed

            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload))

            if ret.status_code == 200:
                print("Feed set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def set_exposure(self, exposure):
        if  self.check_exposure(exposure):
            url = self.settings_url
            
            self.payload["exposure"] = exposure
            
            ret = requests.put(url, headers = self.headers, data = json.dumps(self.payload)) 

            if ret.status_code == 200:
                print("Exposure set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))  

    def enable_auto_exposure(self, autoExpo):
        if self.enable_check(autoExpo) == True:
            url = self.settings_url
            
            self.payload["autoExpo"] = autoExpo

            ret = requests.put(url, headers = self.headers, data= json.dumps(self.payload))    

            if ret.status_code == 200:
                print("Auto exposure set successfully.")
            else:
                raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_config(self):
        url = self.settings_url

        ret = requests.get(url)

        if ret.status_code == 200:
            self.print_json(ret.content)
            return json.loads(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_calibration_matrix(self):
        url = self.imgCalibration_url

        ret = requests.get(url)        

        if ret.status_code == 200:           
            self.print_json(ret.content)
            return json.loads(ret.content)
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def capture_opencv_image(self):
        if not self.opencv_flag:
            import cv2
        r = requests.get(self.stream_url, stream=True)
        if(r.status_code == 200):
            bytes = b""
            for chunk in r.iter_content(chunk_size=1024):
                bytes += chunk
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b+2]
                    bytes = bytes[b+2:]
                    i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    return i
        else:
            raise ValueError("Received unexpected status code {}".format(r.status_code))

    def check_feed(self, feed):
        if feed == "00" or feed == "11":
            return True
        else:
            raise ValueError("Invalid Feed")

    def check_resolution(self, width, height):
        try:
            if self.valid_resolution[width] == height:
                return True 
            elif self.valid_resolution[width][0] == height or self.valid_resolution[width][1] == height:
                return True
        except:
            raise ValueError("Invalid Resolution")

    def check_case(self, case):
        if case == 1 or case == 2:
            return True
        else: 
            raise ValueError("Invalid Case.")

    def check_image_rotation(self, rotation):
        if rotation == "0" or rotation == "90_CW" or rotation == "90_CCW" or rotation == "180":
            return True
        else: 
            raise ValueError("Invalid Rotation.")

    def check_hdmi_rotation(self, rotation):
        if rotation == "0" or rotation == "90_CW" or rotation == "90_CCW" or rotation == "180":
            return True
        else: 
            raise ValueError("Invalid Rotation.")
    
    def check_exposure(self, exposure):
        if 0 <= exposure <= 0.03:
            return True
        else:
            raise ValueError("Invalid Exposure.")

    def enable_check(self, enable):
        if enable == 0 or enable == 1:
            return True
        else:
            raise ValueError("Invalid Entry.") 

    def print_json(self, content):
        obj = json.loads(content)
        
        json_formatted_str = json.dumps(obj, indent = 4)

        print(json_formatted_str)
