# -*- coding: UTF-8 -*-
import random
import string

import qanty.common.models as models


def test_get_user(qanty_client, user):
    target_user_id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

    user = qanty_client.get_user(user_id=user.id, target_user_id=target_user_id)
    assert isinstance(user, models.User)


def test_get_user_by_email(qanty_client, user):
    user = qanty_client.get_user(user_id=user.id, target_email="user@qanty.com")
    assert isinstance(user, models.User)
