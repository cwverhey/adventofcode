#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 01 2023

@author: caspar
"""

import re
import requests
import tempfile
import statistics
import os
import json
from bs4 import BeautifulSoup as bs
import numpy as np
from collections import Counter, defaultdict, deque
from math import lcm
import keyring
import html2text
import time
from pprint import pprint
from itertools import combinations
import pandas as pd

AOC_LOGIN_CONFIGFILE = os.path.expanduser('~/.config/adventofcode-login.json')

# cat '{"user":"cwverhey","cookie":""}' > AOC_LOGIN_CONFIGFILE
# keyring.set_password("aoc", "cwverhey", "staplebatteryhorse")


def update_cookie():

    with open(AOC_LOGIN_CONFIGFILE, 'r') as f:
        config = json.load(f)

    sess = requests.Session()

    r = sess.get("https://adventofcode.com/auth/github")
    soup = bs(r.content)
    formhtml = soup.find("form")

    # action = formhtml.attrs.get("action", '') # not safe; don't send data to just any server
    # method = formhtml.attrs.get("method", "get").lower()
    inputs = {i.attrs['name']: i.attrs.get('value','') for i in formhtml.find_all('input')}

    inputs['login'] = config['user']
    inputs['password'] = keyring.get_password("aoc", config['user'])

    r = sess.post("https://github.com/session", data=inputs)

    for c in sess.cookies:
        if c.name == "session" and c.domain == ".adventofcode.com":
            config['cookie'] = 'session='+c.value

    with open(AOC_LOGIN_CONFIGFILE, 'w') as f:
        json.dump(config, f)


def get_task(day, year = 2023):

    with open(AOC_LOGIN_CONFIGFILE, 'r') as f:
        config = json.load(f)

    url = f'https://adventofcode.com/{year}/day/{day}'
    r = requests.get(url, headers={'cookie': config['cookie']})
    soup = bs(r.content)
    main = soup.find('main')
    text = html2text.html2text(str(main))
    text = text.split('You can also [Shareon\n[Twitter]')[0].strip()
    print(text)


def get_input(day, year = 2023, numeric = False, raw = False, lines = False):

    with open(AOC_LOGIN_CONFIGFILE, 'r') as f:
        config = json.load(f)

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    result = requests.get(url, headers={'cookie': config['cookie']}).text
    if raw: return result
    if lines: return result.split('\n')[:-1]
    result = result.split()
    if numeric: result = [int(x) for x in result]
    return result


def submit(day, part, answer, year = 2023):

    with open(AOC_LOGIN_CONFIGFILE, 'r') as f:
        config = json.load(f)

    url = f'https://adventofcode.com/{year}/day/{day}/answer'
    r = requests.post(url, headers={'cookie': config['cookie']}, data={'level': part, 'answer': answer})

    soup = bs(r.content)
    main = soup.find('main')

    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(str(main))
    text = text.split('You can [Shareon\n[Twitter]')[0].strip()
    print(text)


def flatten(lst):
    flat_list = []
    for row in lst:
        flat_list += row
    return flat_list

def unique(lst):
    return list(set(lst))