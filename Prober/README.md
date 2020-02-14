# Computer-Networks
Computer Networks course assignments

### Requirements
1. nmap (Network Manager): `sudo apt install nmap`
2. pandas: `pip3 install pandas`

### Usage
1. Create a file, `keys.py` with variable `sudo_password = "<your_password>"`
2. Give execute permission to `script.sh`. Run: `chmod +x script.sh`
3. Run: `python probe.py <ip> <number of probes per hour>`
4. `Ctrl + C` to exit. This automatically saves all acquired probe results.

### Example
<pre><code>python probe.py 172.16.118.1/23 5</code></pre>