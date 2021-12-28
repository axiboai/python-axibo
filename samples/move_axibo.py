from axibo import Axibo
import time

if __name__ == '__main__':
    import random
    x = Axibo("192.168.2.39")
    
    if not x.pan.connected():
        raise Exception("Pan axis not connected")

    #only need to call once to set motor parameters as needed
    x.pan.set_motor_configuration()
    x.tilt.set_motor_configuration()
    x.update()

    #can be called whenever you like, the below example shows moving two axis
    #multiple axis can be moved in the same way
    #for fastest results call update() after all moves have been loaded
    x.pan.move_absolute(angle=10, speed=5)
    x.tilt.move_absolute(angle=5, speed=2.5)
    x.update()

    while 1:
        print(x.pan.current_position(), x.pan.is_busy())

