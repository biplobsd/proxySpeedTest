# Contact me http://t.me/biplob_sd
import socket
import os
import time
import re
import shutil
import socks
import argparse
from threading import Thread
from sockshandler import SocksiPyHandler
from urllib import request, error
import sys
from datetime import datetime
from tqdm import tqdm, trange
from pathlib import Path


def process_cli():
    parser = argparse.ArgumentParser(
        description="""THIS'S SIMPLE SCRIPT ONLY TEST PROXY DOWNLOADING SPEED.
        GET PROXY FROM WEBSITE.""",
        usage='%(prog)s [-h][-v][-nb] -u URL [-f FILE]',
        epilog="(c) ALPHA4D (Biplob SD) 2019, e-mail: biplobsd11@gmail.com",
        add_help=False
    )
    parent_group = parser.add_argument_group(
        title="Options"
    )
    parent_group.add_argument(
        "-h",
        "--help",
        action="help",
        help="Help"
    )
    parent_group.add_argument(
        "-v",
        "--version",
        action="version",
        help="Display the version number",
        version="%(prog)s version: 1.0.0"
    )
    parent_group.add_argument(
        "-u",
        "--url",
        help="URL of the mirror. Add custom mirror (default is GoogleFiber)",
        metavar="URL"
    )
    parent_group.add_argument(
        "-f",
        "--file",
        help="Proxy list file. (default is proxys.txt)",
        metavar="FILE"
    )
    parent_group.add_argument(
        "-nb",
        "--no-banner",
        action="store_true",
        default=False,
        help="Do not print banner (default is False)"
    )
    return parser


def sec_to_mins(seconds):
    a = str(round((seconds % 3600)//60))
    b = str(round((seconds % 3600) % 60))
    d = f"{a} m {b} s"
    return d


class TqdmUpTo(tqdm):

    def update_to(self, b=1, bsize=1, tsize=None):

        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def downloadChunk(idx, proxy_ip, filename, mirror):
    Sbar = "{desc}: {percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} {rate_fmt}{postfix}"
    try:
        if protocol == 'http':
            proxy_handler = request.ProxyHandler({'http': proxy_ip, })
        if protocol == 'https':
            proxy_handler = request.ProxyHandler({'https': proxy_ip, })
        elif protocol == 'sock4':
            ip, port = proxy_ip.split(':')
            proxy_handler = SocksiPyHandler(socks.SOCKS4, ip, int(port))
        elif protocol == 'sock5':
            ip, port = proxy_ip.split(':')
            proxy_handler = SocksiPyHandler(socks.SOCKS5, ip, int(port))
        opener = request.build_opener(proxy_handler)
        request.install_opener(opener)
        with TqdmUpTo(bar_format=Sbar, unit='B', unit_scale=True, unit_divisor=1024, miniters=1, position=idx, desc=f'Thread {idx}', leave=False) as pbar:
            request.urlretrieve(
                mirror, filename=f'{filename}{idx}', reporthook=pbar.update_to, data=None)
            request.urlcleanup()
            return True
    except error.URLError:
        print(f"\nThread {idx}. Invalid ip or timeout for {proxy_ip}")
        return False
    except ConnectionResetError:
        print(f"\nThread {idx}. Could not connect to {proxy_ip}")
        return False
    except IndexError:
        print(f'\nThread {idx}. You must provide a testing IP:PORT proxy')
        return False
    except socket.timeout:
        print(f"\nThread {idx}. Invalid ip or timeout for {proxy_ip}")
        return False
    except KeyboardInterrupt:
        print(f"\nThread no: {idx}. Exited by User.")
        exit()


def speedTest(ip):
    global NAMESPACE
    if NAMESPACE.url is None:
        # mirror = 'http://speedtest.tele2.net/1MB.zip'
        mirror = 'http://provo.speed.googlefiber.net:3004/download?size=1048576'
    else:
        mirror = NAMESPACE.url
    global protocol
    socket.setdefaulttimeout(5)
    filename = 'test.zip'
    for i in range(3):
        if os.path.exists(f'{filename}{i}'):
            os.remove(f'{filename}{i}')
    timeStart = datetime.now()
    proxy_ip = ip.strip()
    print(f"\n\n\nSERVER: {proxy_ip} | Downloading ...")
    downloaders = [
        Thread(
            target=downloadChunk,
            args=(idx, proxy_ip, filename, mirror),
        )
        for idx in range(3)
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
    delta = round(float((timeEnd - timeStart).seconds) +
                  float(str('0.' + str((timeEnd - timeStart).microseconds))), 3)
    speed = round(filesize / 1024) / delta

    for i in range(3):
        if os.path.exists(f'{filename}{i}'):
            os.remove(f'{filename}{i}')

    unsort.append(
        {'ip': f'SERVER: {proxy_ip}  \t\tSIZE: {filesizeM}MB \tTIME: {sec_to_mins(delta)}\t', 'speed': int(speed)})
    return 'Done'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def cleanupOutputs():
    if int(time.strftime('%d')) % 3 == 0:
        if os.path.exists('outputs'):
            if sum(f.stat().st_size for f in Path('outputs').glob('**/*') if f.is_file()) >= 2000000:
                try:
                    shutil.rmtree('outputs')
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}")


def inputdata(filename, arrayname=[]):
    if not os.path.exists('proxys.txt'):
        open('proxys.txt', 'a+').close()

    with open(filename, 'r+') as handle:
        htmlRO = handle.read()

    x = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}[\s:\t][0-9]{1,5}", htmlRO)
    for line in range(len(x)):
        x[line] = re.sub('[\s]', ':', x[line])

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
    elif default == 'http':
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
            print("\n\nError : Please respond with Number[1/2/3/4] \n")


parser = process_cli()
NAMESPACE = parser.parse_args(sys.argv[1:])
unsort = []
sort = []
filelogs = ""
if NAMESPACE.file is None:
    proxyslist = inputdata('proxys.txt')
else:
    proxyslist = inputdata(NAMESPACE.file)

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

if NAMESPACE.no_banner:
    banner = ""


if not len(proxyslist) == 0:
    cleanupOutputs()
    print(banner)
    print(f'{len(proxyslist)} proxy ip:port found!')
    protocol = whichProtocol("\n\nWhich's protocol do you want use with ")
    clear()
    print(banner)
    for i in trange(len(proxyslist), unit='A', unit_scale=True, unit_divisor=1024, miniters=1, desc=f'Completed', position=0, leave=True):
        p = speedTest(proxyslist[i])
        clear()
        print(banner)
        if p:
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
