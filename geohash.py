#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a slightly modified version of the example implementation from the geo-
hashing wiki (http://wiki.xkcd.com/geohashing/Implementations/Libraries/Python).
"""

from hashlib import md5
from datetime import timedelta
from struct import unpack_from
from urllib.request import urlopen
from cachetools import LRUCache
import config

# dow jones cache
dow_cache = LRUCache(maxsize=config.cache_size)

def dow(date):
    if date in dow_cache:
        return dow_cache[date]
    else:
        dow_cache[date] = \
            42 #urlopen(date.strftime(config.dow_url)).read().decode('utf-8')
        return dow_cache[date]


def calculate(loc, date):
    if loc[1] < -30:
        td30 = 0
    else:           # 30W rule
        td30 = 1
    if loc[0] < 0:
        south = -1
    else:
        south = 1
    if loc[1] < 0:
        west = -1
    else:
        west = 1
    djia = dow(date - timedelta(td30))
    sum = md5(bytes('{0}-{1}'.format(date, djia), 'utf-8')).digest()
    return [d * (abs(a) + f) for (d, f, a) in zip((south, west),
            [x / 2. ** 64 for x in unpack_from('>QQ', sum)], loc)]
