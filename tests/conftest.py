# -*- coding: UTF-8 -*-

import pytest

from qanty import Qanty

TEST_AUTH_TOKEN = "test_auth_token"
TEST_COMPANY_ID = "test_company_id"


@pytest.fixture(scope="session")
def qanty():
    """
    Fixture that returns an instance of the Qanty class with a given auth token.

    Returns:
        Qanty: An instance of the Qanty class.
    """
    return Qanty(auth_token=TEST_AUTH_TOKEN, company_id=TEST_COMPANY_ID)
