import qanty.common.models as models


def test_get_roles(qanty_client, user):
    roles = qanty_client.get_roles(user_id=user.id)
    assert isinstance(roles, list)

    if len(roles) > 0:
        assert all(isinstance(role, models.UserRole) for role in roles)
