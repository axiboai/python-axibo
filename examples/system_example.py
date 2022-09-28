from axibo import Axibo
import time

if __name__ == '__main__':    
    #Change for you Axibos IP Address
    x = Axibo("10.42.0.1")

    x.system.get_bluetooth_status()

    time.sleep(1)

    #Put device in pairing mode before this code is ran
    x.system.configure_bluetooth(3, "98:CD:E3:23:42:BD")

    #Wait for the visual indicator
    connected_status = input("Enter y when connected: ")

    if connected_status == 'y':
        x.system.get_bluetooth_status()
        
        delete_status = input("Would you like to delete this bluetooth device (y/n): ")

        if delete_status == 'y':
            x.system.configure_bluetooth(2, "98:CD:E3:23:42:BD")

            time.sleep(2)

            x.system.get_bluetooth_status()

    

    
