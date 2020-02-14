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
if nopph < 1 or nopph > 360:
    print('Number of probes per hour must be >= 1 and <= 360')
    exit(1)

# Time interval(in seconds) between successive probes
tibsp = 3600 // nopph

if os.path.isfile('data.csv'):
    df = pd.read_csv('data.csv')
    i = len(df)
else:
    df = pd.DataFrame(columns=['Time of the day', 'Number of hosts up'])
    i = 0

last_second = -1

try:
    while(True):
        now = datetime.now()
        curr_second = now.minute * 60 + now.second
        if curr_second != last_second and curr_second % tibsp == 0:
            # Number of hosts up
            nohu = run(ip)
            now = now.replace(microsecond=0)
            df.loc[i] = [now, nohu]
            print([str(now), nohu])
            i += 1
            last_second = curr_second
        time.sleep(0.5)
except:
    print(traceback.format_exc())
    df.to_csv('data.csv', index=False)