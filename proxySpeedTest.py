#Contact me http://t.me/biplob_sd
import sys, threading, socket, os, time, re
from datetime import datetime
from collections import OrderedDict
from urllib import error
import urllib.request
from tqdm import tqdm, trange
import socks
import sockshandler


def my_hook(t):
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        if tsize not in (None, -1):
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


class TqdmUpTo(tqdm):

    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def sec_to_mins(seconds):
	a=str(round((seconds%3600)//60))
	b=str(round((seconds%3600)%60))
	d="{} m {} s".format(a, b)
	return d


def speedTest(ip):
	#mirror = 'http://speedtest.tele2.net/1MB.zip'
	mirror = 'http://provo.speed.googlefiber.net:3004/download?size=1048576'
	global protocol
	socket.setdefaulttimeout(5)
	filename = 'test.zip'

	for i in range(3):
		if os.path.exists(f'{filename}{i}'):
			os.remove(f'{filename}{i}')

	timeStart = datetime.now()
	proxy_ip = ip.strip()
	print(f"\n\n\nSERVER: {proxy_ip} | Downloading ...")
	def downloadChunk(idx,_):
		try:
			urllib.request.urlcleanup()
			if protocol == 'http':
				proxy_handler = urllib.request.ProxyHandler({'http': proxy_ip,})
			if protocol == 'https':
				proxy_handler = urllib.request.ProxyHandler({'https': proxy_ip,})
			elif protocol == 'sock4':
				ip,port = proxy_ip.split(':')
				proxy_handler = sockshandler.SocksiPyHandler(socks.SOCKS4, ip, int(port))
			elif protocol == 'sock5':
				ip,port = proxy_ip.split(':')
				proxy_handler = sockshandler.SocksiPyHandler(socks.SOCKS5, ip, int(port))

			opener = urllib.request.build_opener(proxy_handler)
			urllib.request.install_opener(opener)
			with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=f'Thread {idx}') as t:
						urllib.request.urlretrieve(mirror, filename=f'{filename}{idx}', reporthook=t.update_to,data=None)
		except error.URLError:
			 return print(f"\nThread {idx}. Invalid ip or timeout for {proxy_ip}")
		except ConnectionResetError:
			return print(f"\nThread {idx}. Could not connect to {proxy_ip}")
		except IndexError:
			return print(f'\nThread {idx}. You must provide a testing IP:PORT proxy in the cmd line')
		except socket.timeout:
			return print(f"\nThread {idx}. Invalid ip or timeout for {proxy_ip}")
		except KeyboardInterrupt:
			print("\nThread no: {idx}. Exited by User.")

	downloaders = [
		threading.Thread(
			target=downloadChunk,
			args=(idx,_),
		)
		for idx,_ in enumerate(range(3))
		]

	for th in downloaders:
		th.start()
	for th in downloaders:
		th.join()

	timeEnd = datetime.now()
	filesize = 0
	for i in range(3):
		try:
			filesize = filesize + os.path.getsize(f'{filename}{i}')
		except FileNotFoundError:
			continue

	filesizeM = round(filesize / pow(1024, 2), 2)
	delta = round(float((timeEnd - timeStart).seconds) + float(str('0.' + str((timeEnd - timeStart).microseconds))), 3)
	speed = round(filesize / 1024) / delta


	for i in range(3):
		if os.path.exists(f'{filename}{i}'):
			os.remove(f'{filename}{i}')

	unsort.append({'ip':f'SERVER: {proxy_ip}  \t\tSIZE: {filesizeM}MB \tTIME: {sec_to_mins(delta)}\t','speed':int(speed)})
	return 'Done'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def inputdata(filename, arrayname=[]):
	open('proxys.txt', 'a+').close()
	with open(filename, 'r+') as handle:
		htmlRO = handle.read()

	x = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}[\s:][0-9]{1,5}",htmlRO)
	for line in range(len(x)):
		x[line] = re.sub('[\s]',':', x[line])

	with open('proxys.txt', 'w+') as p:
		for line in x:
			p.write(line+'\n')
	return x

def saveOutput(data):
	global protocol
	global filelogs
	if len(data) == 1:
		try:
			os.mkdir('outputs')
		except FileExistsError:
			pass
		filelogs = f"outputs/{time.strftime('%Y%m%d_%H_%M_%S')}.txt"
	with open(filelogs, 'w+') as w:
		w.write(f"{time.strftime('%X %x %Z')} | Protocol {protocol} \n")
		for line in data:
			w.write(line['ip']+'\t'+str(line['speed'])+' KB/s\n')



def whichProtocol(question, default="http"):
	valid = {"1": 'http', "2": 'https', "3": 'sock4',
 		"4": 'sock5', 'http': 'http'}
	if default is None:
		prompt = "\n\n1. http\n2. https\n3. sock4\n4. sock5 "
	elif default is 'http':
		prompt = f" \n\n1. http\n2. https\n3. sock4\n4. sock5"
	else:
		raise ValueError("\n\ninvalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(prompt + question+f'[default={default}]: ')
		choice = input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			clear()
			sys.stdout.write("\n\nError : Please respond with Number[1/2/3/4] \n")

unsort = []
sort = []
filelogs = ""
proxyslist = inputdata('proxys.txt')
banner = """
                             _____                     _ _______        _
                            / ____|                   | |__   __|      | |
  _ __  _ __ _____  ___   _| (___  _ __   ___  ___  __| |  | | ___  ___| |_
 | '_ \| '__/ _ \ \/ / | | |\___ \| '_ \ / _ \/ _ \/ _` |  | |/ _ \/ __| __|
 | |_) | | | (_) >  <| |_| |____) | |_) |  __/  __/ (_| |  | |  __/\__ \ |_
 | .__/|_|  \___/_/\_\\__,  |_____/| .__/ \___|\___|\__,_|  |_|\___||___/\__|
 | |                   __/ |      | |
 |_|                  |___/       |_|                       -dev-by-Alpha4d-
"""

if not len(proxyslist) == 0:
	print(banner)
	print(f'{len(proxyslist)} proxy ip:port found!')
	protocol = whichProtocol("\n\nWhich's protocol do you want use with ")
	clear()
	print(banner)
	for i in trange(len(proxyslist),unit='A', unit_scale=True, unit_divisor=1024, miniters=1, desc=f'Completed'):
		p = speedTest(proxyslist[i])
		clear()
		print(banner)
		if not (p[0] == 'C' or p[0] == 'I' or p[0] == 'Y'):
			sort = sorted(
			    unsort,
			    key=lambda x: x['speed'], reverse=True)
		saveOutput(sort)
		print(f"\nSort as Speed: (Top 10) | Protocol : {protocol}")
		count = 0
		for p in sort:
			count += 1
			print(p['ip']+'\t'+str(p['speed'])+' KB/s')
			if count == 10:
				break
		print("\n")
else:
	print("Import some proxys(IP:prot) in proxys.txt file.")
