# This web client polls a given route with GET request. Depending on the response, it can perfom an emergency reset
# of the repository.
# This will be used only in emergency cases and to save the relays.
# This client is intended to be as small as possible, as it will never be updatable


import requests
import time
import os
URL = "https://api.b-iot.ch/relays/emergency"
SLEEP_TIME = 600 # 10 minutes
  

# Get the relayID from the config:
relay_id = "TODO"

PARAMS = {'relayID':relayID}

while True:  
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()

    repo_url = data['results'][0]['repoURL']
    force_flag = data['results'][0]['force']

    if force_flag:
        # Delete possible old repo
        os.system(f"rm -rf /home/pi/biot/relays_biot && cd /home/pi/biot && git clone \"{repo_url}\" && sudo reboot")
        

    time.sleep(SLEEP_TIME)