from datetime import datetime, timedelta
from collections import defaultdict
import re

parse_re = re.compile(
    r'^\[(?P<date>.*)\] (?P<event>.*)$')
parse2_re = re.compile(
    r'Guard #(?P<name>\d+) begins shift')

def parseDate(text):
    return datetime.strptime(text, '%Y-%m-%d %H:%M')

def parseGuard(text):
    return parse2_re.match(text).group('name')

def iterminutes(a, b):
    delta = timedelta(minutes=1)
    while a < b:
        yield a.minute
        a = a + delta

def parse(text):
    m = parse_re.match(text)
    date = parseDate(m.group('date'))
    event = m.group('event')
    if 'begins shift' in event:
        guardId = parseGuard(event)
        return date, 'start', guardId
    if 'falls asleep' in event:
        return date, 'asleep', None
    if 'wakes up' in event:
        return date, 'wakeup', None
    return None

def solve(data):
    idata = map(parse, data)
    idata = sorted(idata, key=lambda x: x[0])
    make_guard = lambda: defaultdict(int)
    guards = defaultdict(make_guard)
    guard, st = None, None
    for dt, event, guardId in idata:
        if event == 'start':
            guard = guards[guardId]
        if event == 'asleep':
            st = dt
        if event == 'wakeup':
            for minute in iterminutes(st, dt):
                guard[minute] += 1
            st = None
    dd = {k: sum(v.values()) for k, v in guards.items()}
    most_sleepy = max(dd.items(), key=lambda x: x[1])[0]
    most_min = max(guards[most_sleepy].items(), key=lambda x: x[1])[0]
    return int(most_sleepy) * most_min

def solve2(data):
    idata = map(parse, data)
    idata = sorted(idata, key=lambda x: x[0])
    make_guard = lambda: defaultdict(int)
    guards = defaultdict(make_guard)
    guard, st = None, None
    for dt, event, guardId in idata:
        if event == 'start':
            guard = guards[guardId]
        if event == 'asleep':
            st = dt
        if event == 'wakeup':
            for minute in iterminutes(st, dt):
                guard[minute] += 1
            st = None
    dd = {k: max(v.values(), default=0) for k, v in guards.items()}
    most_sleepy = max(dd.items(), key=lambda x: x[1])[0]
    most_min = max(guards[most_sleepy].items(), key=lambda x: x[1])[0]
    return int(most_sleepy) * most_min

def test1():
    data = """[1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    [1518-11-01 00:30] falls asleep
    [1518-11-01 00:55] wakes up
    [1518-11-01 23:58] Guard #99 begins shift
    [1518-11-02 00:40] falls asleep
    [1518-11-02 00:50] wakes up
    [1518-11-03 00:05] Guard #10 begins shift
    [1518-11-03 00:24] falls asleep
    [1518-11-03 00:29] wakes up
    [1518-11-04 00:02] Guard #99 begins shift
    [1518-11-04 00:36] falls asleep
    [1518-11-04 00:46] wakes up
    [1518-11-05 00:03] Guard #99 begins shift
    [1518-11-05 00:45] falls asleep
    [1518-11-05 00:55] wakes up"""
    idata = list(map(str.strip, data.split('\n')))
    assert solve(idata) == 240

def main():
    with open('day4.txt', 'r') as f:
        data = f.readlines()
    print('Part 1:', solve(data))
    print('Part 2:', solve2(data))

if __name__ == '__main__':
    test1()
    main()
