from turtle import up, update
import requests
import json

#Add trigger case to the waypoint.

class Waypoint():

    def __init__(self, dev):

        self.dev = dev
        self.waypoint_url = 'http://{}:2200/v1/wp_list'.format(self.dev.ip)

        self.headers = {'Content-Type': 'application/json'}

        self.payload = {
            "listName": "default101",
            "points": [
                {
                "pan": 0,
                "tilt": 0,
                "slider": 0,
                "focus" : 0,
                "zoom": 0,
                "duration": "00:00:00.000"
                }
            ]
        }

    def help(self):
        print("\n---> Waypoint Help <---\n")
        
        print("Function: get_waypoint_list() \nDesciption: Returns all the waypoints currently saved to Axibo.\n")
        
        print("Function: get_waypoint() \nDesciption: Returns only the waypoint specified.\n")
        
        print("Function: delete_waypoint() \nDesciption: Deletes the specified waypoint.\n")
        
        print("Function: create_waypoint() \nDesciption: Creates a new waypoint.\n")
        
        print("Function: add_point() \nDesciption: Adds a point to a pre-existing waypoint.\n")

        print("Function: edit_point() \nDescription: Edits a pre-existing waypoint.\n")
    
    def create_waypoint_json(self, json_format):
        url = self.waypoint_url

        ret = requests.posts(url, headers = self.headers, data = json.dumps(json_format))

        if ret.status_code == 200:
            print("Waypoint created successfully.")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def create_waypoint(self, name, pan = 0, tilt = 0, slide = 0, focus = 0, zoom = 0, duration = "00:00:00.000"):
        url = self.waypoint_url

        self.payload["listName"] = name
        self.payload["points"][0]["pan"] = pan
        self.payload["points"][0]["tilt"] = tilt
        self.payload["points"][0]["slider"] = slide
        self.payload["points"][0]["focus"] = focus
        self.payload["points"][0]["zoom"] = zoom
        self.payload["points"][0]["duration"] = duration

        ret = requests.post(url, headers = self.headers, data = json.dumps(self.payload))

        if ret.status_code == 200:
            print("Waypoint created successfully.")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def add_point(self, name, pan = 0, tilt = 0, slide = 0, focus = 0, zoom = 0, duration = "00:00:00.000"):
        url = self.waypoint_url
        index = 0

        current = requests.get(url)

        update_points = json.loads(current.content)

        for i in update_points:
            if i['listName'] == name:
                print(index)
                break
            index += 1

        update_points[index]["points"].append({
            "pan": pan,
            "tilt": tilt,
            "slider": slide,
            "focus": focus,
            "zoom": zoom,
            "duration": duration
            })

        payload = {
            "listName": name,
            "points": update_points[index]["points"]
        }

        self.delete_waypoint(name)

        ret = requests.post(url, headers = self.headers, data = json.dumps(payload))

        if ret.status_code == 200:
            print(f"Added point to {name} at position {index} successfully.")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def edit_point(self, name, point, pan = 0, tilt = 0, slide = 0, focus = 0, zoom = 0, duration = "00:00:00"):
        url = 'http://{}:2200/v1/wp_list/{}'.format(self.dev.ip, name)

        current = requests.get(url)

        update_points = json.loads(current.content)

        print(update_points["points"][point])

        update_points["points"][point] = {
            "pan": pan,
            "tilt": tilt,
            "slider": slide,
            "focus": focus,
            "zoom": zoom,
            "duration": duration
            }

        payload = {
            "listName": name,
            "points": update_points["points"]
        }

        ret = requests.put(url, headers = self.headers, data = json.dumps(payload))

        if ret.status_code == 200:
            print(f"Edited point in {name} at position {point} successfully.")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def delete_waypoint(self, name):
        url = 'http://{}:2200/v1/wp_list/{}'.format(self.dev.ip, name)

        payload = {}
        headers = {}

        ret = requests.delete(url, headers = headers, data = payload)

        if ret.status_code == 200:
            self.print_json(ret.content)
            print("Waypoint deleted successfully.")
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def get_waypoint_list(self):
        url = self.waypoint_url
        
        ret = requests.get(url)

        if ret.status_code == 200:
            self.print_json(ret.content)        
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))
    
    def get_waypoint(self, name):
        url = 'http://{}:2200/v1/wp_list/{}'.format(self.dev.ip, name)
        ret = requests.get(url)

        if ret.status_code == 200:
            self.print_json(ret.content)
            return json.loads(ret.content)    
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))

    def waypoint_run(self, name):
        url = 'http://{}:2200/v1/direct-control/move-waypoints/{}'.format(self.dev.ip, name)

        payload = {
            "trigger":{
            "trigCase":0,
            "timeSpacing":0,
            "pauseAmount":0,
            },
            "sequencer":0,
        }

        ret = requests.put(url, headers = self.headers, data = json.dumps(payload))

        if ret.status_code == 200:
            print("Running waypoint.") 
        else:
            raise ValueError("Received unexpected status code {}".format(ret.status_code))       
        
    def print_json(self, content):
        obj = json.loads(content)
        
        json_formatted_str = json.dumps(obj, indent = 4)

        print(json_formatted_str)