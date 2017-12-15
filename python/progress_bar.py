# -*- coding: utf-8 -*-
# 将编码格式改为 utf-8 之后，可以使用中文注释
from tqdm import tqdm, trange
from time import sleep

# nested progress bars
for i in tqdm(xrange(4), desc='1st loop'):
    for j in tqdm(xrange(100), desc='2nd loop', leave=False):
        sleep(0.01)

# 在进行 progress bar 时不能直接使用 print 输出
# Since tqdm uses a simple printing mechanism to display progress bars,
# you should not write any message in the terminal using print() while a progressbar is open.
# To write messages in the terminal without any collision with tqdm bar display, a .write() method is provided:
bar = trange(10)
for i in bar:
    # Print using tqdm class method .write()
    sleep(0.1)
    if not (i % 3):
        tqdm.write("Done task %i" % i)
    # Can also use bar.write()
