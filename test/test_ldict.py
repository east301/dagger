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
