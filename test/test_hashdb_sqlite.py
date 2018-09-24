import os
import dagger


def fwrite(txt, fn):
    open(fn, 'w').write(txt)


def rm(fn):
    try:
        os.remove(fn)
    except:     # NOQA
        pass


def test_load_missing():
    d = dagger.hashdb_sqlite()
    d.load()


def test_get_missing():
    d = dagger.hashdb_sqlite()
    assert not d.get('tmp')


def test_update(tmpdir):
    os.chdir(tmpdir)

    f = 'tmp.sqlite'
    rm(f)

    fwrite('', 'tmp')

    d = dagger.hashdb_sqlite(f)
    d.load()
    d.update('tmp')
    h1 = d.get('tmp')
    d.export()

    fwrite('stuff', 'tmp')
    d.load()
    d.update('tmp')
    h2 = d.get('tmp')

    assert h1
    assert h2
    assert h1 != h2


def test_load_memory(tmpdir):
    os.chdir(tmpdir)

    f = 'tmp.sqlite'
    rm(f)

    fwrite('', 'tmp')

    d = dagger.hashdb_sqlite(f)
    d.load()
    d.update('tmp')
    d.export()
    del d

    d = dagger.hashdb_sqlite(f, True)
    d.load()
    h = d.get('tmp')
    assert h and len(h[0]) > 10


def test_export(tmpdir):
    os.chdir(tmpdir)

    f1 = 'tmp1'
    f2 = 'tmp2'
    f3 = 'tmp3'
    fwrite('1', f1)
    fwrite('1', f2)
    fwrite('3', f3)

    f = 'tmp.sqlite'
    rm(f)

    d = dagger.hashdb_sqlite(f)
    d.load()
    d.update(f1)
    d.update(f2)
    d.update(f3)
    d.export()
    del d

    d = dagger.hashdb_sqlite(f)
    d.load()

    h1 = d.get(f1)
    h2 = d.get(f2)
    h3 = d.get(f3)

    assert d.db and h1 and h1 == h2 and h1 != h3


def test_export_memory(tmpdir):
    os.chdir(tmpdir)

    f1 = 'tmp1'
    f2 = 'tmp2'
    f3 = 'tmp3'
    fwrite('1', f1)
    fwrite('1', f2)
    fwrite('3', f3)
    f = 'tmp.sqlite'
    rm(f)

    d = dagger.hashdb_sqlite(f, True)
    d.load()
    d.update(f1)
    d.update(f2)
    d.update(f3)
    d.export()
    del d

    d = dagger.hashdb_sqlite(f, True)
    d.load()

    h1 = d.get(f1)
    h2 = d.get(f2)
    h3 = d.get(f3)

    assert d.db and h1 and h1 == h2 and h1 != h3
