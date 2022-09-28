from axibo.axibo import Axibo

if __name__ == '__main__':
    #Change for you AXIBO IP Address
    x = Axibo("10.42.0.1")
    x.camera.set_resolution(640, 480)
    x.ai.enable_pose(1) # enable and disable pose detection
    x.ai.enable_tracking(True) # start tracking
    x.ai.set_object("HEAD") # select object
    x.ai.set_init_policy("left") # position of the object in the view
    x.ai.set_slide_speed(0) # speed of slider from 0 to 1
    x.ai.set_pan_speed(1)
    x.ai.set_tilt_speed(1)
    x.ai.set_transition_speed(1) # speed of transitioning from one object to another from 0 to 1

