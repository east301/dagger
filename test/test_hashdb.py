import os

import dagger


def test_md5_missing():
    assert dagger.hashdb.md5('tmp.missing') is None


def test_md5(tmpdir):
    os.chdir(tmpdir)
    os.system('touch tmp')
    assert dagger.hashdb.md5('tmp')


def test_load_missing():
    d = dagger.hashdb()
    d.load()


def test_get_missing():
    d = dagger.hashdb()
    assert not d.get('tmp')


def test_update(tmpdir):
    os.chdir(tmpdir)
    os.system('touch tmp')
    d = dagger.hashdb()
    d.update('tmp')
    assert d.get('tmp')


def test_export(tmpdir):
    os.chdir(tmpdir)
    os.system('echo 1 > tmp1')
    os.system('echo 1 > tmp2')
    os.system('echo 2 > tmp3')
    d = dagger.hashdb('tmp.db')
    d.update('tmp1')
    d.update('tmp2')
    d.update('tmp3')
    d.export()
    del d

    lut = dict([x.split(',') for x in open('tmp.db').readlines()])

    assert lut
    assert len(lut['tmp1']) > 1
    assert lut['tmp1'] == lut['tmp2']
    assert lut['tmp1'] != lut['tmp3']


def test_load(tmpdir):
    test_export(tmpdir)

    d = dagger.hashdb('tmp.db')
    d.load()
    assert d.db
    assert len(d.db['tmp1']) > 1
    assert d.db['tmp1'] == d.db['tmp2']
    assert d.db['tmp1'] != d.db['tmp3']
