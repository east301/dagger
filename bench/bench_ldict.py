import sys
import time

import dagger


if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    n = 100000

a = range(n)
d = dagger.ldict(a)

tic = time.time()
while d.head:
    d.remove(d.head.data)

toc = time.time()
print(toc - tic)
