# -*- coding: UTF-8 -*-
import os

import pytest

from qanty import Qanty
from qanty.common.models import UserRole, User


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


@pytest.fixture(scope="session")
def user():
    """
    Fixture that returns a test user object for use in session-scoped tests.

    Returns:
        User: A test user object with a test role.
    """
    role = UserRole(
        id="test_user_role_id",
        name="Test Role",
        roleGroup="Test Role Group",
        enabled=True,
        hidden=False,
        deleted=False,
        rules=[],
    )

    return User(
        id="test_user_id",
        name="Test User",
        lastName="",
        docId="",
        email="test_email",
        enabled=True,
        hidden=False,
        deleted=False,
        role=role,
    )
