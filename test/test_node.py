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

import dagger


def test_add(tmpdir):
    os.chdir(tmpdir)
    os.system('touch tmp tmp.1')
    n1 = dagger.node('tmp')
    n2 = dagger.node('tmp.1')
    n1.add(n2)

    assert len(n1.nodes)


def test_format_abs(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp')
    n = dagger.node('tmp')

    # Should return '*/tmp'.
    s = n.format('%a')
    assert len(s) > 4


def test_format_date(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp')
    n = dagger.node('tmp')

    # Should return 'yyyy-mm-dd'.
    s = n.format('%d')
    assert len(s) > 8


def test_format_time(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp')
    n = dagger.node('tmp')

    # Should return 'hh:mm:ss'.
    s = n.format('%t')
    assert len(s) > 6


def test_format_base(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp.1')
    n = dagger.node('tmp.1')

    s = n.format('%b')
    assert s == 'tmp.1'


def test_format_base_dot(tmpdir):
    os.chdir(tmpdir)

    os.system('touch .tmp')
    n = dagger.node('.tmp')

    s = n.format('%b')
    assert s == '.tmp'


def test_format_root(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp.1')
    n = dagger.node('tmp.1')

    s = n.format('%r')
    assert s == 'tmp'


def test_format_root_dot(tmpdir):
    os.chdir(tmpdir)

    os.system('touch .tmp')
    n = dagger.node('.tmp')

    s = n.format('%r')
    assert s == '.tmp'


def test_update_time(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp')
    n = dagger.node('tmp')

    n.update(time=True, hash=False)
    assert n.time > 0


def test_update_hash(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp')
    n = dagger.node('tmp')

    n.update(time=False, hash=True)
    assert n.hash


def test_missing_is_stale(tmpdir):
    os.chdir(tmpdir)

    os.system('touch tmp1')
    n1 = dagger.node('tmp1')
    n1.update()

    n2 = dagger.node('tmp_missing')
    n2.update()

    assert n1.stale is None
    assert n2.stale
