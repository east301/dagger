import time
import sys

if len(sys.argv) > 1:
  n = int(sys.argv[1])
else:
  n = 100000

a = range(n)
d = dict([(v,v) for v in a])

tic = time.time()
while a:
  v = a[0] 
  d.pop( v )
  a.remove(v)
  
toc = time.time()
print toc-tic
