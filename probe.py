import subprocess
import sys
from keys import sudo_password
from datetime import datetime
import pandas as pd
import traceback
import time
import os

'''
Usage:
    Run: python probe.py <ip> <number of probes per hour>
'''

def run(ip):
    '''
    Returns number of hosts which are running for the given CIDR IP address
    '''

    # Create a subprocess to run the bash script
    process = subprocess.Popen('./script.sh ' + sudo_password + ' ' + ip, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    output = output.decode('ascii')
    output = int(output[1:])
    return output

# IP address to probe (uses CIDR addressing)
ip = sys.argv[1]

# Number of probes per hour
nopph = int(sys.argv[2])


# Time interval between successive probes
tibsp = 60 // nopph

if os.path.isfile('data.csv'):
    df = pd.read_csv('data.csv')
    i = len(df)
else:
    df = pd.DataFrame(columns=['Time of the day', 'Number of hosts up'])
    i = 0

last_minute = -1

try:
    while(True):
        now = datetime.now()
        curr_minute = now.minute
        if curr_minute != last_minute and curr_minute % tibsp == 0:
            # Number of hosts up
            nohu = run(ip)
            now = now.replace(microsecond=0)
            df.loc[i] = [now, nohu]
            print([str(now), nohu])
            i += 1
            last_minute = curr_minute
        time.sleep(1)
except:
    print(traceback.format_exc())
    df.to_csv('data.csv', index=False)