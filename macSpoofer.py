import subprocess, random, datetime, time, argparse, sys
from pync import Notifier

def letter(x):
	if (x == 10):
		return 'a'
	elif (x == 11):
		return 'b'
	elif (x == 12):
		return 'c'
	elif (x == 13):
		return 'd'
	elif (x == 14):
		return 'e'
	elif (x == 15):
		return 'f'

def createRandomMac():
	mac = ""
	i = 0
	while (i < 12):
		if (i % 2 == 0 and i != 0):
			mac += ':'
		value = random.randint(0, 15)
		if (value > 9):
			value = letter(value)
		mac += str(value)
		i += 1
	return mac

# Parse command line arguments
parser = argparse.ArgumentParser(description = 'Spoofs MAC address to random value at given interface at the given' +
	'time interval')
parser.add_argument('-i', '--interface', dest = 'interface', help = 'Network interface to spoof MAC address of',
	type = str, metavar = 'INTERFACE')
parser.add_argument('-t', '--time-interval', dest = 'timeInterval', help = 'How often to spoof MAC address, in minutes.' + 
	'Defaults to 5', type = int, metavar = 'TIME')
interface = ''
timeInterval = 5
args = parser.parse_args()
if (args.interface != None):
	interface = args.interface
else:
	print('Error: no interface or time interval specified')
	sys.exit(1)
if (args.timeInterval != None):
	timeInterval = int(args.timeInterval)
else:
	print('Error: no interface or time interval specified')
	sys.exit(1)

while (True):
	currentTime = datetime.datetime.now()
	mac = createRandomMac()
	try:
		subprocess.check_call('sudo ifconfig ' + interface + ' ether ' + mac, shell = True)
		time.sleep(1)
		subprocess.check_call('sudo ifconfig ' + interface + ' down', shell = True)
		time.sleep(1)
		subprocess.check_call('sudo ifconfig ' + interface + ' up', shell = True)
		print(currentTime.strftime("%m/%d/%Y %I:%M %p") + ": Spoofed MAC address to '" + mac + "'")
	except subprocess.CalledProcessError:
		Notifier.notify("Error: failed to spoof MAC address")
		print("Error: failed to spoof MAC address to '" + mac + "'")
	time.sleep(timeInterval * 60) # Amount of time between MAC address changes
