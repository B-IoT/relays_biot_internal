# This script is started from rc.local run as user pi

cd $(dirname $0)

while ! (ping -c 1 -W 1 1.2.3.4 | grep -q 'statistics'); do
    echo "Waiting for 1.2.3.4 - network interface might be down..."
    sleep 10
done

pi pip3 install -r requirements.txt
pi python3 emergency_web_client.py >> /home/pi/biot/logs/emergency_web_client.py