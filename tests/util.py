def assert_equal_lists(l1, l2):
    assert len(l1) == len(l2)
    assert str(sorted(l1)) == str(sorted(l2))
