# Dagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dagger.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012 Remik Ziemlinski

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
