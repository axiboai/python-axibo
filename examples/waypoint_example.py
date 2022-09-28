from axibo import Axibo

if __name__ == '__main__':
    #Change for you Axibos IP Address
    x = Axibo("10.42.0.1")

    #Delete waypoints
    #Uncomment if you have ran this program once already
    x.waypoint.delete_waypoint("example")

    #Creates a default point 0
    x.waypoint.create_waypoint(name = "example")

    x.waypoint.add_point(name = "example", pan = 0, tilt = 0, slide = 50, duration = "00:00:07.000")

    x.waypoint.add_point(name = "example", pan = 45, tilt = 0, slide = 0, duration = "00:00:07.000")

    #Point 3
    x.waypoint.add_point(name = "example", pan = -45, tilt = 0, slide = 0, duration = "00:00:07.000")

    x.waypoint.add_point(name = "example", pan = 0, tilt = 45, slide = 0, duration = "00:00:05.000")

    x.waypoint.add_point(name = "example", pan = 0, tilt = -45, slide = 0, duration = "00:00:08.000")

    x.waypoint.edit_point("example", 3, pan = -90, tilt = 0, slide = 0, duration = "00:00:12.000")

    x.waypoint.waypoint_run("example")





