# This web client polls a given route with GET request. Depending on the response, it can perfom an emergency reset
# of the repository.
# This will be used only in emergency cases and to save the relays.
# This client is intended to be as small as possible, as it will never be updatable


import requests
import time
import os
URL = "https://api.b-iot.ch/api/relays/emergency"
SLEEP_TIME = 600 # 10 minutes
DEFAULT_RELAY_ID = "relay_0"
  

# Get the relayID from the config:
relay_id = DEFAULT_RELAY_ID
try:
    f = open("/home/pi/biot/config/.config", "r")
    lines = f.readlines()
    for l in lines:
        if "relayID" in l:
            relay_id = l.split(":")[1]  
            relay_id = relay_id.replace('"', '')
            relay_id = relay_id.replace(',', '')
            relay_id = relay_id.replace('\n', '')
            relay_id = relay_id.replace('\r', '')
            break
    
    f.close()
except IOError:
    # No .config file, send the default id
    relay_id = DEFAULT_RELAY_ID

PARAMS = {"relayID":relay_id}

print("Emergency web client has started!")

while True:  
    time.sleep(SLEEP_TIME)
    try:
        print("Emergency web client: send request...")
        r = requests.get(url = URL, params = PARAMS)
        if r.status_code == 200:
            data = r.json()

            repo_url = data['repoURL']
            force_flag = data['forceReset']

            print(f"Emergency web client: repo url: {repo_url}")
            if force_flag:
                print("EMERGENCY: Resetting repository")
                os.system(f"rm -rf /home/pi/biot/relays_biot && cd /home/pi/biot && git clone \"{repo_url}\" && chmod +x /home/pi/biot/relays_biot/start.sh && sudo reboot")
            else:
                print("Emergency web client: no reset needed")
        else:
            print(f"Emergency web client: error in received response, status_code = {r.status_code}")
    except:
        print("Emergency web client: ERROR while get response or decoding response!")