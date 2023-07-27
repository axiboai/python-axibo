import os
import socket    
import multiprocessing
import subprocess
import requests
import json

def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """
    
    ip_list = list()
    
    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    
    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]
    
    for p in pool:
        p.start()
    
    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))
    
    for p in pool:
        jobs.put(None)
    
    for p in pool:
        p.join()
    
    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list


def find_axibos():
    lst = map_network()
    axibo_name = []
    axibo_ip = []
    global_index = 0
    json_output={"axibos":[]}
    for ip in lst:
        try:
            system_info_url = 'http://{}:2200/v1/system/info'.format(ip)
            ret = requests.get(system_info_url, timeout = 0.2)
            if ret.status_code == 200: 
                axibo_name.append("AXIBO-{}".format(json.loads(ret.content)["serialNum"]))
                axibo_ip.append(ip)
                new_axibo = {"name": "AXIBO-{}".format(str(json.loads(ret.content)["serialNum"])), "ip": str(ip)}
                json_output["axibos"].append(new_axibo)
                print("Index {}: AXIBO-{} --> {}".format(global_index, json.loads(ret.content)["serialNum"], ip))
                global_index += 1
            # else:
            #     raise ValueError("Received unexpected status code {}".format(ret.status_code))
        except:
            pass
                

    if(len(axibo_name)==0):
        return "none"
    else:
        print("Software selected",json_output["axibos"][0]["name"])
        return json_output["axibos"][0]["ip"]
    