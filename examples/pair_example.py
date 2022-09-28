from axibo import Axibo

#Change for your AXIBOs IP Address
pair = Axibo("10.42.0.1")

#Change the MAC address to the MAC address of your wireless controller
pair.system.configure_bluetooth(2, "98:CD:E3:23:42:BD")