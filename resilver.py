import json, sys, re, subprocess, time, threading
from pushover import init, Client

TIME_INTERVAL = 900 # 15 minutes
user_key = None
application_key = None
client = None

# Fetch the Pushover credentials from a json file
def get_credentials():
    try:
        credentials = json.load(open('credentials.json'))
        global user_key
        global application_key
        user_key = credentials['user_key']
        application_key = credentials['application_key']
    except:
        sys.exit('Credentials not found!')

# Initialise the Pushover client
def initialise_client():
    client = Client(user_key, api_token=application_key)
    return client

# Send a pushover notification containing the given status
def notify(status):
    client.send_message('Resilvering status is at {}%'.format(status), title="Resilver Status Update")

# Get the current percentage status of the resilver
def get_status():
    reg = '[0-9]+.[0-9]+%'
    raw = subprocess.run(['zpool','status','MediaVolume'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return float(re.findall(reg,raw)[0].replace('%',''))

# Check the current resilver status and send it in a notification via Pushover
def monitor_resilver():
    notify(get_status())

get_credentials()
client = initialise_client()
resilver = threading.Event()

# Check the resilver status every 15 minutes
while not resilver.wait(TIME_INTERVAL):
    monitor_resilver()
