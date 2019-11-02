#!/usr/bin/env python
import sys, threading, time, math, socket, os, subprocess
from collections import OrderedDict
from urllib import error, request
import urllib.request
from tqdm import tqdm

def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst


def speedTest(ip):
	#mirror = "https://drive.google.com/uc?id=0Bzkrq-7orwGScTAxNkFDaTM0Rkk&authuser=0&export=download"
	mirror = 'http://speedtest.tele2.net/1MB.zip'
	socket.setdefaulttimeout(30)
	filename = '1MB.zip'
	start = time.time()
	sizeInBytes = '1048576'
	dataDict = {}
	ranges = buildRange(int(sizeInBytes), 3)
	proxy_ip = ip.strip()
	def downloadChunk(idx, irange):
		try:
			proxy_handler = urllib.request.ProxyHandler({'http': proxy_ip})
			opener = urllib.request.build_opener(proxy_handler)
			urllib.request.install_opener(opener)
			req = urllib.request.Request(mirror)
			req.add_header('Range', f'bytes={irange}')
			dataDict[idx] = urllib.request.urlopen(req).read()

		except error.URLError:
			 return print(f"\nInvalid ip or timeout for {proxy_ip}")
		except ConnectionResetError:
			return print(f"\nCould not connect to {proxy_ip}")
		except IndexError:
			return print(f'\nYou must provide a testing IP:PORT proxy in the cmd line')
		except socket.timeout:
			return print(f"\nInvalid ip or timeout for {proxy_ip}")
		except KeyboardInterrupt:
			print("\n\nExited by User.")

	downloaders = [
		threading.Thread(
			target=downloadChunk,
			args=(idx, irange),
		)
		for idx,irange in enumerate(ranges)
		]

	for th in downloaders:
		th.start()
	for th in downloaders:
		th.join()


	if os.path.exists(filename):
		os.remove(filename)

	with open(filename, 'wb') as fh:
		for _idx,chunk in sorted(dataDict.items()):
			fh.write(chunk)

	delta = time.time() - start
	filesize = os.path.getsize(filename)
	ratio = filesize/(delta*1024)
	return f"Proxy {proxy_ip} has download speed:{math.floor(ratio)} KB/s"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

unsort = []
sort = []
proxyslist = []
open('proxys.txt', 'a+').close()
handle = open('proxys.txt')
for line in handle:
	if not len(line.strip()) == 0 :
		proxyslist.append(line)
handle.close()

try:
	if not len(proxyslist) == 0:
		for i in tqdm(proxyslist):
			p = speedTest(i)
			clear()
			print(p)
			if not (p[0] == 'C' or p[0] == 'I' or p[0] == 'Y'):
				ip , kb = p.split('d:')
				kb1 , kb = kb.split(' KB/s')
				unsort.append({'ip':ip+'d','speed':int(kb1)})
				sort = sorted(
				    unsort,
				    key=lambda x: x['speed'], reverse=True)
			print("\nSort as Speed: (Top 10)")
			count = 0
			for p in sort:
				count += 1
				print(p['ip']+'\t'+str(p['speed'])+' KB/s')
				if count == 10:
					break
			print("\nChecking ...")
	else:
		print("Import some proxys(IP:prot) in proxys.txt file.")
except KeyboardInterrupt:
	print("\n\nExited by User.")
