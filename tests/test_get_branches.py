# -*- coding: UTF-8 -*-

import qanty.common.models as models


def test_get_branches(qanty):

    assert isinstance(qanty.company_id, str)
    assert isinstance(qanty.client.headers.get("Authorization"), str)

    response = qanty.get_branches()
    assert isinstance(response, list)


def test_get_deleted_branches(qanty):
    response = qanty.get_branches(get_deleted=True)
    assert isinstance(response, list)


def test_get_branches_with_filters(qanty):
    response = qanty.get_branches(filters={"branch_groups": ["group1", "group2"]})
    assert isinstance(response, list)
