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

import os

import pytest

import dagger
from test_dagger import fill, delete, touch


def test_iter():
    d = dagger.dagger()
    d.add('1', ['2', '3', '4'])
    d.add('4', ['5', '6'])
    d.stale('6')
    d.run(allpaths=True)

    iter = d.iter()
    ldict = iter.ldict

    for name in '1 4 6'.split():
        assert ldict.get(d.nodes[name])

    for name in '2 3 5'.split():
        assert ldict.get(d.nodes[name])


def _run_test_iterator(names=[], remove='', nexts=[]):
    d = dagger.dagger()
    d.add('1', ['2', '3', '4'])
    d.add('4', ['5', '6'])
    d.add('7', ['6'])
    d.stale('5')
    d.stale('6')
    d.run(allpaths=True)

    remove = remove.split()

    it = d.iter(names)
    next = it.next(2)
    while remove:
        assert next == nexts[0]

    try:
        name = remove.pop(0)
        nexts.pop(0)
        it.remove(name)
    except:     # NOQA
        pytest.fail()

    next = it.next(2)


# def test_iterator_all():
#     return _run_test_iterator([], '5 6 7 4 1', [['5','6'], ['6'], ['4','7'], ['4'], ['1']])


# def test_iterator_names():
#     return _run_test_iterator(['6'], '6 4 1 7', [['6'], ['4','7'], ['1','7'], ['7']])


def test_missing(tmpdir):
    os.chdir(tmpdir)

    # Create empty files.
    fill(['1', '2', '3'])

    # Ensure missing file.
    try:
        os.remove('missing')
    except: # NOQA
        pass

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('2', ['missing'])
    d.run(allpaths=True)

    it = d.iter()
    next = []

    items = it.next()
    next.extend(items)
    if items:
        it.remove(items[0])

    items = it.next()
    next.extend(items)
    if items:
        it.remove(items[0])

    items = it.next()
    next.extend(items)
    if items:
        it.remove(items[0])

    assert next == ['missing', '2', '1']


def test_top_fresh(tmpdir):
    os.chdir(tmpdir)

    all = '1 2 3 4 5 6'.split()
    touch(all, 0)

    # Ensure missing file.
    delete('missing')

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('2', ['missing'])
    d.add('4', ['5'])
    d.add('5', ['6'])
    d.run(allpaths=True)

    it = d.iter(['4'])
    next4 = it.next()

    it = d.iter(['2'])
    next2 = it.next()

    return not next4 and next2


def test_top_stale(tmpdir):
    os.chdir(tmpdir)

    all = '1 2 3 4 5 6'.split()
    touch(all, 0)

    # Ensure missing file.
    delete('missing')

    try:
        os.remove('6')
    except:     # NOQA
        pass

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('2', ['missing'])
    d.add('4', ['5'])
    d.add('5', ['6'])
    d.run(allpaths=True)

    it = d.iter(['4'])

    assert it.next() == ['4']
