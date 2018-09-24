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
# Copyright 2018 east301

import dagger


def test_all():
    a = [1, 2, 3, 4]
    d = dagger.ldict(a)
    assert d.head and d.head.data == 1
    assert d.tail and d.tail.data == 4

    for x in a:
        assert d.get(x) and d.get(x).data == x

    for x, y, z in [[1, 2, 4], [3, 2, 4], [4, 2, 2], [999, 2, 2]]:
        d.remove(x)
        assert d.head and d.head.data == y
        assert d.tail and d.tail.data == z

    d.remove(2)
    assert not d.head
    assert not d.tail
