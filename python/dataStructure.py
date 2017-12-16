# -*- coding: utf-8 -*-

from collections import defaultdict, deque


def test_queue():
    q = deque(maxlen=30)
    for i in range(100):
        q.append(i)
    print q
    l = list(q)
    print l


if __name__ == '__main__':
    test_queue()
