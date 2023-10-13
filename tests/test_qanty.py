# -*- coding: UTF-8 -*-


def test_qanty(qanty):
    assert isinstance(qanty.company_id, str)
    assert qanty.company_id == "test_company_id"