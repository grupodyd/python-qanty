# -*- coding: UTF-8 -*-
import os

import pytest

from qanty import Qanty


TEST_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TEST_COMPANY_ID = os.environ.get("COMPANY_ID")


@pytest.fixture(scope="session")
def qanty():
    """
    Fixture that returns an instance of the Qanty class with a given auth token.

    Returns:
        Qanty: An instance of the Qanty class.
    """
    return Qanty(auth_token=TEST_AUTH_TOKEN, company_id=TEST_COMPANY_ID)
