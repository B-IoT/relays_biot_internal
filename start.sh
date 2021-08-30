cd $(dirname $0)

pip3 install -r requirements.txt
python3 emergency_web_client.py >> /home/pi/biot/logs/emergency_web_client.py