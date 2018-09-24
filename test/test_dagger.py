import os
import time

import dagger


def delete(files):
    if type(files) not in [type([]), type(())]:
        files = [files]

    for f in files:
        try:
            os.remove(f)
        except:     # NOQA
            pass


def fill(files, text=''):
    """Write text to all files listed."""
    for f in files:
        fh = open(f, 'w')
        fh.write(text)
        fh.close()


def touch(names, t=None):
    """Set (future) atime/mtime per file name."""
    if type(names) not in [type([]), type(())]:
        names = [names]

    if t is None:
        t = time.time() + 1

    for n in names:
        if not os.path.exists(n):
            fill(n)
        os.utime(n, (t, t))


def paths_equal(dag, names, truth):
    """Check if each node has paths in truth dict."""
    for name in names:
        n = dag.get(name)
        if not n.paths:
            if n.paths != truth[name]:
                return False
        elif dag.pathnames(name) != truth[name]:
            return False

    return True


def stale_dict(dag, names):
    """Create dict of stale values for just named files."""
    out = {}
    for n in names:
        out[n] = dag.get(n).stale
    return out


def test_pathnames():
    d = dagger.dagger()
    d.add('1', ['2', '3'])
    n1 = d.get('1')
    n2 = d.get('2')
    n3 = d.get('3')
    n1.paths = [[n2, n3]]
    p = d.pathnames('1')
    assert p and p == [['2', '3']]


def test_run_order(tmpdir):
    """Check graph walk order."""
    os.chdir(tmpdir)

    all = '1 2 3 4 5 6 7'.split()
    fill(all)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])
    d.run(allpaths=False)
    names = [n.name for n in d.order.list]
    assert names == '2 4 5 3 1 7 6'.split()


def test_run_paths(tmpdir):
    """Check graph depth-first path for each node."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    all = '1 2 3 4 5 6 7'.split()
    fill(all)
    d.run(allpaths=False)

    truth = {
        '1': None,
        '2': [['1']],
        '3': [['1'], ['6']],
        '4': [['3', '1']],
        '5': [['3', '1']],
        '6': None,
        '7': [['6']],
    }
    assert paths_equal(d, all, truth)


def test_run_allpaths(tmpdir):
    """Check all graph paths possible."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    all = '1 2 3 4 5 6 7'.split()
    fill(all)

    d.run(allpaths=True)

    truth = {
        '1': None,
        '2': [['1']],
        '3': [['1'], ['6']],
        '4': [['3', '1'], ['3', '6']],
        '5': [['3', '1'], ['3', '6']],
        '6': None,
        '7': [['6']],
    }
    assert paths_equal(d, all, truth)


def test_force(tmpdir, allpaths=False):
    """Check forcing staleness."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    all = '1 2 3 4 5 6 7'.split()
    touch(all)

    d.resetnodes()
    d.stale('1', 1)
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth

    touch(all)
    d.resetnodes()
    d.forced.clear()
    d.stale('2', 1)
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 1, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states2 = stale_dict(d, all)
    assert states2 == truth

    touch(all)
    d.resetnodes()
    d.forced.clear()
    d.stale('3', 1)
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 0, '6': 1, '7': 0}
    states3 = stale_dict(d, all)
    assert states3 == truth

    touch(all)
    d.resetnodes()
    d.forced.clear()
    d.stale('5', 1)
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 1, '6': 1, '7': 0}
    states4 = stale_dict(d, all)
    assert states4 == truth


def test_force_allpaths(tmpdir):
    test_force(tmpdir, allpaths=True)


def test_time(tmpdir, allpaths=False):
    """Check stale when file timestamps are old."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    all = '1 2 3 4 5 6 7'.split()
    fill(all)
    touch(all, 0)
    touch('1')

    d.run(allpaths=allpaths)
    truth = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth

    touch(all, 0)
    touch('2')

    d.resetnodes()
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states2 = stale_dict(d, all)
    assert states2 == truth

    touch(all, 0)
    touch('3')

    d.resetnodes()
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 0, '4': 0, '5': 0, '6': 1, '7': 0}
    states3 = stale_dict(d, all)
    assert states3 == truth

    touch(all, 0)
    touch('4')

    d.resetnodes()
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 0, '6': 1, '7': 0}
    states4 = stale_dict(d, all)
    assert states4 == truth

    touch(all, 0)
    touch('5')

    d.resetnodes()
    d.run(allpaths=allpaths)
    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 0, '6': 1, '7': 0}
    states5 = stale_dict(d, all)
    assert states5 == truth

    touch(all, 0)
    touch('6')

    d.resetnodes()
    d.run(allpaths=allpaths)
    truth = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states6 = stale_dict(d, all)
    assert states6 == truth

    touch(all, 0)
    touch('7')

    d.resetnodes()
    d.run(allpaths=allpaths)
    truth = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 1, '7': 0}
    states7 = stale_dict(d, all)
    assert states7 == truth


def test_time_allpaths(tmpdir):
    return test_time(tmpdir, allpaths=1)


def test_hash_missing(tmpdir):
    """Check stale when file hashes missing."""
    os.chdir(tmpdir)

    d = dagger.dagger('tmp.missing')
    d.hashall = True
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    all = '1 2 3 4 5 6 7'.split()
    fill(all)

    d.run()
    truth = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states = stale_dict(d, all)
    assert states == truth


def test_hash(tmpdir):
    """Check stale when file hashes change."""
    os.chdir(tmpdir)

    all = '1 2 3 4 5 6 7'.split()
    fill(all, '')

    db = dagger.hashdb('tmp.db')
    for f in all:
        db.update(f)
    db.export()

    fill(['5'], 'test')

    d = dagger.dagger('tmp.db')
    d.hashall = True
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    d.run()
    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 1, '6': 1, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth


def test_dot(tmpdir):
    """Test exporting dot graph file."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])

    all = '1 2 3 4 5 6 7'.split()
    fill(all)
    touch(all, 0)
    touch('5')

    f = 'tmp.dot'
    d.run()
    d.dot(out=f, color=1)

    assert os.path.exists(f)
    text = open(f).read()
    assert '1 [fillcolor = "#ff' in text
    assert '3 [fillcolor = "#ff' in text
    assert '6 [fillcolor = "#ff' in text
    assert '5 [fillcolor = white]' in text


def test_phony(tmpdir):
    """Make a missing file phony and make sure nothing is stale."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])
    d.phony('3')

    all = '1 2 3 4 5 6 7'.split()
    touch(all, 0)
    delete('3')
    d.run()

    truth = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth


def test_phony_force_stale(tmpdir):
    """Make a missing file phony and force it to stale."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])
    d.phony('3')

    all = '1 2 3 4 5 6 7'.split()
    touch(all, 0)
    delete('3')
    d.stale('3')
    d.run()

    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 0, '6': 1, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])
    d.phony('3')

    all = '1 2 3 4 5 6 7'.split()
    touch(all, 0)
    delete('3')
    d.stale('4')
    d.run()

    truth = {'1': 1, '2': 0, '3': 1, '4': 1, '5': 0, '6': 1, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth


def test_phony_time(tmpdir):
    """Make a missing file phony and ensure stale by stale child (that had older child)."""
    os.chdir(tmpdir)

    d = dagger.dagger()
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])
    d.phony('6')

    all = '1 2 3 4 5 6 7'.split()
    touch(all, 0)
    touch('4', 1)
    d.run()

    truth = {'1': 1, '2': 0, '3': 1, '4': 0, '5': 0, '6': 1, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth


def test_phony_hash(tmpdir):
    """Make a missing file phony and ensure stale by stale child (that had old hash)."""
    os.chdir(tmpdir)

    all = '1 2 3 4 5 6 7'.split()
    fill(all, '')

    db = dagger.hashdb('tmp.db')
    for f in all:
        db.update(f)
    db.export()

    fill(['4'], 'test')

    d = dagger.dagger('tmp.db')
    d.hashall = True
    d.add('1', ['2', '3'])
    d.add('3', ['4', '5'])
    d.add('6', ['3', '7'])
    d.phony('6')
    d.run()

    truth = {'1': 1, '2': 0, '3': 1, '4': 1, '5': 0, '6': 1, '7': 0}
    states1 = stale_dict(d, all)
    assert states1 == truth
