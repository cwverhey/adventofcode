#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# usage:
# import sys; sys.path.append(os.path.dirname(__file__)); import aoc
#
# setup:
# aoc.set_github_login("cwverhey", "staplebatteryhorse")
#   Stores both credentials in the OS keyring, and the username and (eventually) session-cookie in AOC_LOGINFILE.
# aoc.set_ftp_login("cwverhey", "staplebatteryhorse", "example.com")
#   Stores the FTP credentials 

AOC_LOGINFILE = '~/.config/adventofcode-login.json'
AOC_GITDIR = '~/Progs/adventofcode/'


from pathlib import Path
import json
from ftplib import FTP
from io import BytesIO
import subprocess

import requests
from bs4 import BeautifulSoup
import keyring
import html2text

AOC_LOGINFILE_PATH = Path(AOC_LOGINFILE).expanduser().resolve()


def set_github_login(username, password):
    keyring.set_password('AoC GitHub', username, password)

    try:
        with open(AOC_LOGINFILE_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    config['github'] = {'user':username}
    config['aoc'] = {'cookie':''}

    with open(AOC_LOGINFILE_PATH, 'w') as f:
        json.dump(config, f)


def set_ftp_login(username, password, server):
    keyring.set_password('AoC FTP', username, password)

    try:
        with open(AOC_LOGINFILE_PATH, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    config['ftp'] = {'user':username, 'server': server}

    with open(AOC_LOGINFILE_PATH, 'w') as f:
        json.dump(config, f)


def update_cookie(ftp_upload=True):

    with open(AOC_LOGINFILE_PATH, 'r') as f:
        config = json.load(f)

    sess = requests.Session()
    r = sess.get("https://adventofcode.com/auth/github")
    soup = BeautifulSoup(r.content, 'html.parser')
    formhtml = soup.find("form")

    inputs = {i.attrs['name']: i.attrs.get('value','') for i in formhtml.find_all('input')}

    inputs['login'] = config['github']['user']
    inputs['password'] = keyring.get_password("AoC GitHub", config['github']['user'])

    r = sess.post("https://github.com/session", data=inputs)  # don't send data to just any server; hardcode the target instead

    for c in sess.cookies:
        if c.name == "session" and c.domain == ".adventofcode.com":
            config['aoc']['cookie'] = 'session='+c.value

    with open(AOC_LOGINFILE_PATH, 'w') as f:
        json.dump(config, f)

    if ftp_upload:
        ftp = FTP(config['ftp']['server'])
        ftp.login(config['ftp']['user'], keyring.get_password("AoC FTP", config['ftp']['user']))
        file_like_obj = BytesIO(config['aoc']['cookie'].encode('utf-8'))
        ftp.storbinary(f'STOR adventofcode-cookie.txt', file_like_obj)
        ftp.quit()

    print(f'new cookie: {config['aoc']['cookie']}')


def get_task(year, day):
    with open(AOC_LOGINFILE_PATH, 'r') as f:
        config = json.load(f)
    url = f'https://adventofcode.com/{year}/day/{day}'
    req = requests.get(url, headers={'cookie': config['aoc']['cookie']})
    if req.status_code == 500:
        update_cookie()
        return get_task(year, day)
    print(req.status_code)
    return req.content


def task(year, day, part = 'all'):
    html = get_task(year, day)
    main = BeautifulSoup(html, 'html.parser').find('main')
    text = html2text.html2text(str(main))
    text = text.split(r'You can also [Shareon')[0].strip()

    try:
        print(text.split(r'## \--- Part Two ---')[part-1])
    except (KeyError, TypeError):
        print(text)


def examples(year, day, numeric = False, raw = False, lines = False):
    html = get_task(year, day)
    examples = BeautifulSoup(html, 'html.parser').select('pre code')
    examples = [e.text for e in examples]
    examples = list(dict.fromkeys(examples))
    return [parse_input(e, numeric, raw, lines) for e in examples]


def get_input(year, day, numeric = False, raw = False, lines = False):
    with open(AOC_LOGINFILE_PATH, 'r') as f:
        config = json.load(f)
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = requests.get(url, headers={'cookie': config['aoc']['cookie']})
    if req.status_code == 500:
        update_cookie()
        return get_input(year, day, numeric, raw, lines)
    result = req.text
    return parse_input(result, numeric, raw, lines)


def parse_input(text, numeric, raw, lines):
    if raw: return text
    if lines: return text.split('\n')[:-1]
    if numeric: return [int(x) for x in text.split()]
    return text.split()


def submit(year, day, part, answer):

    print(f'Submitting {answer}:')

    with open(AOC_LOGINFILE_PATH, 'r') as f:
        config = json.load(f)

    url = f'https://adventofcode.com/{year}/day/{day}/answer'
    req = requests.post(url, headers={'cookie': config['aoc']['cookie']}, data={'level': part, 'answer': answer})
    if req.status_code == 500:
        update_cookie()
        return submit(year, day, part, answer)

    h = html2text.HTML2Text()
    h.ignore_links = True
    main = BeautifulSoup(req.content, 'html.parser').find('main')
    text = h.handle(str(main))
    text = text.split('You can [Shareon')[0].split('[Return to Day ')[0].strip()
    print(text)


def push_git(year, day, message = None):

    file = f'{year}/day{day:02}.py'
    if message is None:
        message = f'day {day:02}'
    commands = [
        ['git', 'add', file],
        ['git', 'commit', '-m', message],
        ['git', 'log', '--oneline', 'origin/main..HEAD', '--name-only']
    ]
    for command in commands:
        run_cmd(command, str(Path(AOC_GITDIR).expanduser().resolve()))

    if input('push? [Y/N]:').lower() == 'y':
        run_cmd(['git', 'push'], str(Path(AOC_GITDIR).expanduser().resolve()))
    
def run_cmd(cmd, cwd):
    result = subprocess.run(cmd, text=True, capture_output=True, cwd=cwd)
    print(' '.join(cmd))
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)