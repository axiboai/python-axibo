from axibo.axibo import Axibo

if __name__ == '__main__':    
    #Change for you Axibos IP Address
    x = Axibo() # This library can find the Axibos on the network but this takes a bit of time, to speed it up you pass the AXIBO IP address
    x.motion.get_connected_motors() ## get connected motors
    
    ## Preparing a move where
    x.motion.set_absolute_move("slide", 50, 10) # (motor name, position (mm),speed (mm/s))
    x.motion.set_absolute_move("pan", 10, 15) # (motor name, position (deg),speed (deg/s))
    x.motion.set_absolute_move("tilt", 10, 15)

    x.motion.move_now() # excutes move command
    x.motion.move_wait() # waits for the move to finish
    x.motion.set_relative_move("tilt", 10, 15) # relative move
    x.motion.move_now()
    
    x.motion.stop() # stop all motion 
    
    move_json = {"tilt":[0,15],"pan":[0,15],"slide":[0,10]} ## [position,speed]
    x.motion.move_json("absolute", move_json)
    x.motion.move_wait() # waits for the move to finish
    
    move_json = {"tilt":[10,15],"pan":[10,15],"slide":[0,10]} ## [position,speed]
    print(move_json)
    x.motion.stream_move_json("absolute",move_json) ## this uses a websocket for streaming position commands at higher frequency. 
    x.motion.move_wait() # waits for the move to finish

    x.motion.configure_motor("pan", accel=10) ## configure motor parameters 
    config_all = {
        "tilt": {
            "accel": 1,
            "current": 12,
            "maxPos": 45,
            "maxVel": 40,
            "minPos": -45,
        },
        "pan": {
            "accel": 1,
            "current": 12,
            "maxPos": 180,
            "maxVel": 40,
            "minPos": -180,
        },
        "slide": {
            "accel": 1,
            "current": 12,
            "maxPos": 500,
            "maxVel": 10,
            "minPos": 0,
        }
    }

    x.motion.configure_motor_json(config_all) # configure multiple params and multiple motors at the same time
    x.motion.switch_mode("highspeed") ## highspeed/hightorque
    x.motion.packet_conf(1) ## 1/0 on or off ensures the move is excuted, for fast streaming it is not needed
    
    x.motion.calibrate_motor("focus") # calibration
    x.motion.move_wait() # waits for the move to finish
    calibrate_axis = { 
        "pan": {"direction": 0,"homingSpeed": 40,"maxPos": 30,"minPos": -30},
        "tilt": {"direction": 0,"homingSpeed": 40,"maxPos": 30,"minPos": -30}, 
        "slide": {"direction": 0,"homingSpeed": 10}
    }
    x.motion.calibrate_motor_json(calibrate_axis) # calibrates all motors together
    x.motion.get_location()
    
    
    