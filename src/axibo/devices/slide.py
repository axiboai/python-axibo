
class Slide:
    
    def __init__(self, dev):
        self.dev = dev
        self.moveAbsoluteRequest = {}
        self.speed = 5
        self.name = 'slide'
        self.power_scale = 100.0/32.0

    def set_motor_configuration(self, accel=5.0, power=20.0, min_position=-20, max_position=20):
        if min_position > max_position:
            raise Exception("min_position cannot be greater than max_position")
        self.dev.load_action(
            action_type='req_put',
            data = {
                'direct-control/config' :   { self.name: {
                                                "current": int(power/self.power_scale),
                                                "accel": int(accel),
                                                "maxPos": max_position,
                                                "minPos": min_position,
                                            } 
                }
            }
        )


    def set_speed(self, speed):
        self.speed = speed

    def move_absolute(self, angle, speed=None):
        if speed != None:
            out_speed = speed
        else:
            speed = self.speed
        self.dev.load_action(
            action_type='req_put',
            data = {
                'direct-control/move-absolute' : {self.name : [angle, speed] }
            }
        )

    def move_relative(self, angle, speed=None):
        if speed != None:
            out_speed = speed
        else:
            speed = self.speed
        self.dev.load_action(
            action_type='req_put',
            data = {
                'direct-control/move-relative' : {self.name : [angle, speed] }
            }
        )

    def current_position(self):
        return self.dev.stream.device_status_message[self.name]['position']
        
    def is_busy(self):
        return self.dev.stream.device_status_message[self.name]['isBusy']
    
    def connected(self):
        try:
            if self.name in self.dev.stream.device_status_message:
                return True
        except:
            return False
        return False