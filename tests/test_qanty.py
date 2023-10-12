# -*- coding: UTF-8 -*-


def test_get_branches(qanty):
    response = qanty.get_branches()
    assert response is not None