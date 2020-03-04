# Contact me http://t.me/biplob_sd
import os
import re
import sys
import time
import shutil
import argparse
import requests
from pathlib import Path
from urllib import parse
from threading import Thread
from datetime import datetime
from tqdm import tqdm, trange


def process_cli():
    parser = argparse.ArgumentParser(
        description="""THIS'S SIMPLE SCRIPT ONLY TEST PROXY SERVER DOWNLOADING SPEED.
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
        version="%(prog)s version: 1.1.0"
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


def downloadChunk(idx, proxy_ip, filename, mirror):
    global file_size
    try:
        if protocol == 'http':
            proxies = {
                'http': f'http://{proxy_ip}',
                'https': f'http://{proxy_ip}'
            }
        elif protocol == 'https':
            proxies = {
                'http': f'https://{proxy_ip}',
                'https': f'https://{proxy_ip}'
            }
        elif protocol == 'socks4':
            proxies = {
                'http': f'socks4://{proxy_ip}',
                'https': f'socks4://{proxy_ip}'
            }
        elif protocol == 'socks5':
            proxies = {
                'http': f'socks5://{proxy_ip}',
                'https': f'socks5://{proxy_ip}'
            }
        pbar = tqdm(
            total=file_size,
            initial=0,
            dynamic_ncols=True,
            bar_format=Sbar,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            position=idx,
            desc=f'Thread {idx}',
            leave=False
        )
        req = requests.get(
            mirror,
            headers={"Range": "bytes=%s-%s" % (0, file_size)},
            stream=True,
            proxies=proxies,
            timeout=5
        )
        with(open(f'{filename}{idx}', 'ab')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        return True
    except requests.exceptions.ProxyError:
        print(f"\nThread {idx}. Could not connect to {proxy_ip}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"\nThread {idx}. Could not connect to {proxy_ip}")
        return False
    except IndexError:
        print(f'\nThread {idx}. You must provide a testing IP:PORT proxy')
        return False
    except requests.exceptions.ConnectTimeout:
        print(f"\nThread {idx}. ConnectTimeou for {proxy_ip}")
        return False
    except requests.exceptions.ReadTimeout:
        print(f"\nThread {idx}. ReadTimeout for {proxy_ip}")
        return False
    except RuntimeError:
        print(f"\nThread {idx}. Set changed size during iteration. {proxy_ip}")
        return False
    except KeyboardInterrupt:
        print(f"\nThread no: {idx}. Exited by User.")
        exit()


def speedTest(ip):
    global mirror
    global protocol
    filename = 'test'
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
                  float(str('0.' + str((timeEnd -
                                        timeStart).microseconds))), 3)
    speed = round(filesize / 1024) / delta

    for i in range(3):
        if os.path.exists(f'{filename}{i}'):
            os.remove(f'{filename}{i}')

    unsort.append(
        {'ip': f'SERVER: {proxy_ip} ' +
         f'\t\tSIZE: {filesizeM}MB \tTIME: {sec_to_mins(delta)}\t',
         'speed': int(speed)}
    )
    return 'Done'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def cleanupOutputs():
    if int(time.strftime('%d')) % 3 == 0:
        if os.path.exists('outputs'):
            folderElementSize = []
            for f in Path('outputs').glob('**/*'):
                if f.is_file():
                    folderElementSize.append(f.stat().st_size)
            if sum(folderElementSize) >= 2000000:
                try:
                    shutil.rmtree('outputs')
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}")


def inputdata(filename, arrayname=[]):
    if not os.path.exists('proxys.txt'):
        open('proxys.txt', 'a+', encoding="utf-8").close()

    with open(filename, 'r+', encoding="utf-8") as handle:
        htmlRO = handle.read()

    x = re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}[\s:\t][0-9]{1,5}", htmlRO)
    for line in range(len(x)):
        x[line] = re.sub(r'[\s]', ':', x[line])

    with open('proxys.txt', 'w+', encoding="utf-8") as p:
        for line in x:
            p.write(line+'\n')
    return x


def saveOutput(data):
    global protocol
    global filelogs
    global netloc
    global proxyslistname
    if len(data) == 1:
        try:
            os.mkdir('outputs')
        except FileExistsError:
            pass
        filelogs = f"outputs/{time.strftime('%Y%m%d_%H_%M_%S')}.txt"
    with open(filelogs, 'w+') as w:
        w.write(
            f"{time.strftime('%X %x %Z')} | Protocol {protocol} " +
            f"| Mirror: {netloc} | Filename: {proxyslistname} \n"
        )
        for line in data:
            w.write(line['ip']+'\t'+str(line['speed'])+' KB/s\n')


def whichProtocol(question, default="http"):
    valid = {"1": 'http', "2": "https", "3": 'socks4',
             "4": 'socks5', 'http': 'http'}

    if default == 'http':
        prompt = "\n1. http \n2. https \n3. socks4\n4. socks5 "
    else:
        raise ValueError("\n\ninvalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(prompt + question+f'[{default}]: ')
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            clear()
            print("\n\nError : Please respond with Number[1/2/3/4]")


def filelength(url):
    try:
        return int(requests.get(url, stream=True).headers['content-length'])
    except KeyError:
        return int(
            requests.get(
                url,
                headers={'Range': 'bytes=0-'},
                stream=True
            ).headers['Content-Range'].partition('/')[-1]
        )


def fileSmirror(protocol):
    if NAMESPACE.url is None:
        if protocol != "https":
            ps = '\t[1] GoogleFiber' \
                '\n\t[2] bd.archive.ubuntu.com\n\nSelect Mirror : '
            choice = int(input(ps))
            if choice == 1:
                mirror = 'http://provo.speed.googlefiber.net:3004/' \
                    'download?size=1048576'
                file_size = 1048576
            elif choice == 2:
                mirror = 'http://bd.archive.ubuntu.com/ubuntu/' \
                        'indices/override.oneiric.universe'
                file_size = 1062124
        else:
            mirror = 'https://drive.google.com/uc?' \
                'authuser=0&id=0B1MVW1mFO2zmSnZKYlNmT3pjbFE&export=download'
            file_size = filelength(mirror)
    else:
        mirror = NAMESPACE.url
        file_size = filelength(mirror)
    return mirror, file_size


parser = process_cli()
NAMESPACE = parser.parse_args(sys.argv[1:])
unsort = []
sort = []
filelogs = ""
proxyslistname = 'proxys.txt'
if NAMESPACE.file:
    proxyslistname = NAMESPACE.file
proxyslist = inputdata(proxyslistname)
banner = r"""
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
Sbar = "{desc}: {percentage:3.0f}%|{bar}|" \
    "{n_fmt}/{total_fmt} {rate_fmt}{postfix}"

if not len(proxyslist) == 0:
    cleanupOutputs()
    print(banner)
    print(f'{len(proxyslist)} proxy ip:port found!')
    protocol = whichProtocol("\n\nWhich's protocol do you want use with ")
    clear()
    print(banner)
    mirror, file_size = fileSmirror(protocol)
    netloc = parse.urlparse(mirror).netloc
    clear()
    print(banner)
    for i in trange(
        len(proxyslist),
        unit='A',
        unit_scale=True,
        unit_divisor=1024,
        miniters=1,
        desc='Completed',
        position=0,
    ):
        p = speedTest(proxyslist[i])
        clear()
        print(banner)
        if p:
            sort = sorted(
                unsort,
                key=lambda x: x['speed'], reverse=True
            )
        saveOutput(sort)
        print(
            f"\nSort as Speed: (Top 10) | Protocol: {protocol} " +
            f"| Mirror: {netloc} | Filename: {proxyslistname}"
        )
        count = 0
        for p in sort:
            count += 1
            print(p['ip']+'\t'+str(p['speed'])+' KB/s')
            if count == 10:
                break
        print("\n")
else:
    print("Import some proxys(IP:prot) in proxys.txt file.")
