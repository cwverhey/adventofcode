#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(19)

input = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}\n
{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''.split('\n')

input = get_input(19, lines=True)

workflows = {}
for i in input[:input.index('')]:
    name = i[:i.index('{')]
    rules = i[i.index('{')+1:-1].split(',')
    workflows[name] = rules

parts = []
for i in input[input.index('')+1:]:
    if i == '':
        break
    i = re.findall('(\w)=(\d+)', i)
    parts.append({j[0]: int(j[1]) for j in i})

def process(part, workflow):
    for rule in workflows[workflow]:
        print(rule)
        if ':' in rule:
            rule = rule.split(':')
            if rule[0][1] == '>':
                if part[rule[0][0]] <= int(rule[0][2:]):
                    continue
            else:
                if part[rule[0][0]] >= int(rule[0][2:]):
                    continue
            target = rule[1]
        else:
            target = rule

        print('->', target)
        if target in ['A', 'R']:
            return(target)
        else:
            return process(part, target)

accepted_sum = 0
for p in parts:
    if process(p, 'in') == 'A':
        accepted_sum += sum(p.values())

submit(19, 1, accepted_sum)  # 480738

#
# part 2
#

get_task(19)

input = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}\n
{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''.split('\n')

input = get_input(19, lines=True)

workflows = {}
for i in input[:input.index('')]:
    name = i[:i.index('{')]
    rules = i[i.index('{')+1:-1].split(',')
    workflows[name] = rules


def split_range(range, category, comparison, value):  # eg: split_range(range, 'a', '<', 2006)
    if comparison == '<':
        if not range[category][0] < value:
            return [ None, range ] # none of the values in the range matches
        elif range[category][1] < value:
            return [ range, None ] # all of the values in the range match
        else:
            matched_range = copy.deepcopy(range)
            matched_range[category][1] = value - 1
            unmatched_range = copy.deepcopy(range)
            unmatched_range[category][0] = value
            return [ matched_range, unmatched_range ] # split into a matching and a non-matching part

    else:
        # range[category] > value
        if not range[category][1] > value:
            return [ None, range ] # none of the values in the range matches
        elif range[category][0] > value:
            return [ range, None ] # all of the values in the range match
        else:
            matched_range = copy.deepcopy(range)
            matched_range[category][0] = value + 1
            unmatched_range = copy.deepcopy(range)
            unmatched_range[category][1] = value
            return [ matched_range, unmatched_range ] # split into a matching and a non-matching part


accepted_ratings = 0
ranges = [{'name':'in', 'x':[1,4000],'m':[1,4000],'a':[1,4000],'s':[1,4000]}]

while ranges:

    newranges = []
    for range in ranges:
        print(range)

        if range['name'] == 'A':
            accepted_ratings += np.prod([range[cat][1]-range[cat][0]+1 for cat in ['x','m','a','s']])
            continue
        if range['name'] == 'R':
            continue

        for rule in workflows[ range['name'] ]:
            print(rule)
            if ':' in rule:
                rule = rule.split(':')
                matched_range, range = split_range(range, rule[0][0], rule[0][1], int(rule[0][2:]))
                matched_range['name'] = rule[1]
                newranges.append(matched_range)
            else:
                range['name'] = rule
                newranges.append(range)
    ranges = newranges

submit(19, 2, accepted_ratings)  # 131550418841958