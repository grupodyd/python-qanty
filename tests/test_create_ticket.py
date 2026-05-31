# -*- coding: UTF-8 -*-
import json

import httpx
import pytest

import qanty
import qanty.exceptions
from qanty.common import models


def _mock_client(handler):
    client = qanty.Client(auth_token="token", company_id="company-1", endpoint="https://example.test/api")
    client.http_client.close()
    client.http_client = httpx.Client(transport=httpx.MockTransport(handler), headers={"Authorization": "token"})
    return client


def test_create_ticket_sends_current_payload_and_parses_response():
    captured = {}

    def handler(request):
        captured["url"] = str(request.url)
        captured["payload"] = json.loads(request.content.decode())
        return httpx.Response(
            200,
            json={
                "success": True,
                "ticket_name": "A001",
                "ticket_id": "ticket-1",
                "video_call_id": "video-1",
                "vc_jwt": "jwt.token",
            },
        )

    client = _mock_client(handler)
    ticket = client.create_ticket(
        branch_id="branch-1",
        user_id="user-1",
        line_id="line-1",
        details={"reason": "support"},
        mobile_id="mobile-1",
        customer=models.Customer(
            name="Ada",
            last_name="Lovelace",
            doc_type_id="CC",
            doc_id="123",
            email="ada@example.test",
            phone_numbers={"main": "3001234567"},
        ),
        tag_group_name="priority",
        debug=True,
    )

    assert captured["url"] == "https://example.test/api/create_ticket"
    assert captured["payload"] == {
        "company_id": "company-1",
        "branch_id": "branch-1",
        "user_id": "user-1",
        "line_id": "line-1",
        "details": {"reason": "support"},
        "mobile_id": "mobile-1",
        "customer": {
            "name": "Ada",
            "last_name": "Lovelace",
            "doc_type_id": "CC",
            "doc_id": "123",
            "email": "ada@example.test",
            "phone_numbers": {"main": "3001234567"},
        },
        "tag_group_name": "priority",
        "debug": True,
    }
    assert ticket == models.CreatedTicket(ticket_name="A001", ticket_id="ticket-1", video_call_id="video-1", vc_jwt="jwt.token")


def test_created_ticket_builds_video_call_url_only_when_available():
    ticket = models.CreatedTicket(ticket_name="A001", ticket_id="ticket-1", video_call_id="video-1", vc_jwt="jwt.token")
    assert ticket.video_call_url("company-1") == "https://qanty.com/portals/tickets?c=company-1&v=video-1&j=jwt.token"

    ticket_without_video = models.CreatedTicket(ticket_name="A001", ticket_id="ticket-1")
    assert ticket_without_video.video_call_url("company-1") is None


def test_create_ticket_raises_api_error_for_qanty_error_response():
    def handler(request):
        return httpx.Response(
            200,
            json={"success": False, "code": "CREATE_TICKET_FAILED", "msg": "Could not create ticket"},
        )

    client = _mock_client(handler)
    with pytest.raises(qanty.exceptions.ApiError) as exc_info:
        client.create_ticket(branch_id="branch-1", user_id="user-1", line_id="line-1")

    assert exc_info.value.code == "CREATE_TICKET_FAILED"
    assert exc_info.value.msg == "Could not create ticket"
    assert exc_info.value.payload == {"success": False, "code": "CREATE_TICKET_FAILED", "msg": "Could not create ticket"}
