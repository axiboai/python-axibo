import sys
import platform
import ipaddress
import asyncio
import socket

# The coroutine. That function is called using asyncio
async def ping_coroutine(cmd, ip):
    """Async procedure
    ping_coroutine is the coroutine used to send a ping
    """
    # Input:
    #
    # - cmd (string): the command line to be run ("ping XXXXXX")
    # - ip (string): the IP address crrently used in cmd
    #
    # Output:
    # - nbr_host_found (integer, global variable): this number is incremented if
    #   a ping answer has been received
    # - list_of_hosts_found (list of string, global variable): the IP address - which
    #   is "ip" input parameter - is added to this list

    global nbr_host_found, list_of_hosts_found

    # Run the ping shell command
    # stderr is needed in order not to display "Do you want to ping broadcast? Then -b. If not,
    # check your local firewall rules." on Linux systems
    running_coroutine = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    # Suspends the current coroutine allowing other tasks to run
    stdout = await running_coroutine.communicate()

    # Ping OK?
    if "ttl=" in str(stdout).lower():
        # Ping OK
        # 1 host found
        nbr_host_found += 1
        # IP address added to the list of hosts found
        list_of_hosts_found.append(ip)

async def ping_loop():
    """Async procedure
    ping_loop run the list of coroutines, list by list
    """

    global my_tasks, my_list_of_tasks

    # Start the tasks
    # Wait until both tasks are completed
    # Run all commands
    #print("len my_list_of_tasks:" + str(len(my_list_of_tasks)))

    # Read the lists one by one from the list of lists my_list_of_tasks
    for each_task_list in my_list_of_tasks:
        # Start the coroutines one by one from the current list
        for each_coroutine in asyncio.as_completed(each_task_list):
            await each_coroutine

# networkscan class
class Networkscan:

    def __init__(self):
        # Attributes:
        # - nbr_host_found (integer): The number of hosts answering a ping
        # - network (ipaddress object): Object containing network address, netmask, etc.
        # - nbr_host (integer): Number of hosts to ping in the nework
        # - one_ping_param (string): The command line for ping for Windows or Linux
        # - list_of_hosts_found (list of string): List of hosts which answered to the ping command

        self.nbr_host_found = 0
        self.list_of_hosts_found = []
        
        try:
            # Correct input data
            # Use ipaddress library
            self.network = ipaddress.ip_network(self.get_ip())

        except:
            # Problem with input data
            # Display error message and exit
            sys.exit("Incorrect network/prefix " + self.get_ip())

        # Calculate the number of hosts
        self.nbr_host = self.network.num_addresses

        # Network and mask address to remove? (no need if /31)
        if self.network.num_addresses > 2:
            self.nbr_host -= 2

        # Define the ping command used for one ping (Windows and Linux versions are different)
        self.one_ping_param = "ping -n 1 -l 1 -w 1000 " if platform.system().lower() == "windows" else "ping -c 1 -s 1 -w 1 "

    #Edit the IP and add 0/24 at the end
    def get_ip(self):
        ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        dot = '.'

        ip = ip.split('.')

        ip = ip[0] + dot + ip[1] + dot + ip[2] + dot + '0/24'

        return ip

    def run(self):
        """ Method used to create the task lists and to run the coroutine loop """

        global my_tasks, nbr_host_found, list_of_hosts_found, my_list_of_tasks

        # By default at the beginning of every scan there is no host found
        self.nbr_host_found = 0
        self.list_of_hosts_found = []
        my_tasks = []
        nbr_host_found = 0
        list_of_hosts_found = []

        # Every list of coroutine commands are made of 128 ping commands
        # Limiting the number of ping at the same time is needed otherwise
        # we could reach the maximum of shell commands allowed or we can
        # get BlockingIOError errors on Linux systems. This is also the
        # reason why a list of lists is used here.
        i = 128

        # The list of list my_list_of_tasks groups lists of coroutines
        my_list_of_tasks = []
        # By default the current list is added to the list of list my_list_of_tasks
        # A very important concept is that filling the empty list my_tasks will
        # also fill the current list of lists my_list_of_tasks.
        my_list_of_tasks.append(my_tasks)

        # Check if /32 is not used
        if self.network.num_addresses != 1:

            # /32 not used (so there are more than 2 IP adresses)

            # Create the coroutines tasks
            for host in self.network.hosts():

                # cmd has the command line used by the ping command including the ip address
                # example: cmd = "ping -n 1 -l 1 -w 1000 192.168.0.1"
                cmd = self.one_ping_param + str(host)

                # my_tasks is a list with coroutine tasks. It gets 2 parameters: one with
                #  the ping command and the other one with the ip address of the target
                my_tasks.append(ping_coroutine(cmd, str(host)))

                # Decrease the counter of ping commands inside the list
                i -= 1

                # 128 ping in the current list?
                if i <= 0:
                    # Yes
                    i = 128

                    # Clear the current list
                    my_tasks = []
                    # Add a new empty list to the list of list my_list_of_tasks
                    my_list_of_tasks.append(my_tasks)
        else:

            # Yes, just one 1 IP address is used
            # Without the followning code "self.network.hosts()" will not provide
            # the IP address and no ping would be possible for /32 IP addresses

            # Get the IP address; that is ne network IP address actually
            host = str(self.network.network_address)

            # cmd has the command line used by the ping command including the ip address
            # example: cmd = "ping -n 1 -l 1 -w 1000 192.168.0.1"
            cmd = self.one_ping_param + host

            # my_tasks is a list with coroutine tasks. It gets 2 parameters: one with the ping
            #  command and the other one with the ip address of the target
            my_tasks.append(ping_coroutine(cmd, host))

        #print(str(len(my_list_of_tasks)))

        # if Windows is in use then these commands are needed otherwise
        # "asyncio.create_subprocess_shell" will fail
        if platform.system().lower() == "windows":
            asyncio.set_event_loop_policy(
                asyncio.WindowsProactorEventLoopPolicy())

        # Run the coroutine loop
        asyncio.run(ping_loop())

        # Save list of hosts found and number of hosts
        self.list_of_hosts_found = list_of_hosts_found
        self.nbr_host_found = nbr_host_found

