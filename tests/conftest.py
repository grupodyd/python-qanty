# -*- coding: UTF-8 -*-
import os

import pytest

import qanty
from qanty.common.models import User, UserRole

TEST_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TEST_COMPANY_ID = os.environ.get("COMPANY_ID")


@pytest.fixture(scope="session")
def qanty_client():
    """
    Fixture for creating a Qanty client.

    Returns:
        qanty.Client: A Qanty client instance with the specified authentication token and company ID.
    """
    return qanty.Client(auth_token=TEST_AUTH_TOKEN, company_id=TEST_COMPANY_ID)


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
        rules={},
    )

    return User(
        id="test_user_id",
        name="Test User",
        lastName="",
        docId="",
        docType="",
        docTypeId="",
        email="test_email",
        enabled=True,
        hidden=False,
        deleted=False,
        role=role,
        branches=[],
    )
