#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import html
import json
import os
import timeit

os.chdir(WD)
print("~~ Good luck today! ~~")

def getAoC(day, year, example = 0, delHTML = True, strip = True, lines = True, asInt = True, raw = False, cookiefile = os.path.expanduser('~/.config/adventofcode2021-cookie.txt')):
    
    if raw: delHTML = strip = lines = asInt = False
    
    # load JSON file
    filename = f'tasks/AoC_task_{year}_{day}.json'
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = downloadAoC(day, year, cookiefile, True)
    
    # real task
    real = data['real']
    if strip: real = real.strip()
    if lines: real = real.split('\n')
    if asInt:
        try:
            if lines: real = [int(x) for x in real]
            else:     real = int(real) 
        except: pass
    
    # examples
    r = data['examples']
    if isinstance(example, int): r = [r[example]]
    if delHTML: r = [re.sub('<.*?>','',x) for x in r]
    r = [html.unescape(x) for x in r]
    if strip: r = [x.strip() for x in r]
    if lines: r = [x.split('\n') for x in r]
    if asInt:
        try:    r = [[int(x) for x in l] for l in r]
        except: pass
    if isinstance(example, int): ex = r[0]
    else:                        ex = r
    
    # return
    return {'real':real, 'example':ex}


def downloadAoC(day, year, cookiefile = os.path.expanduser('~/.config/adventofcode2021-cookie.txt'), ret = False):
    
    # real task
    url = 'https://adventofcode.com/2021/day/{}/input'.format(day)
    headers = {'cookie': open(cookiefile, 'r').read().strip()}
    real = requests.get(url, headers=headers).text
    
    # examples: get all data inside a <pre><code>
    url = 'https://adventofcode.com/{}/day/{}'.format(year, day)
    result = requests.get(url).text
    examples = re.findall('<pre><code>(.*?)<\/code><\/pre>', result, re.DOTALL)
    
    # save JSON file
    filename = f'tasks/AoC_task_{year}_{day}.json'
    with open(filename, "x") as file:
        json.dump({'real':real, 'examples':examples}, file, indent=4)
    
    # return
    if ret: return({'real':real, 'examples':examples})

def benchmark(stmt, runs):
    b = timeit.timeit(globals=globals(), stmt=stmt, number=runs)
    print('benchmark `{}`: {:.2f}ms (avg {} runs)'.format(stmt, b/runs*1000, runs))