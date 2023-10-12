# -*- coding: UTF-8 -*-
import logging
from typing import Optional, Union

import httpx

import qanty.common.dataclasses

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Qanty:
    url = "https://qanty.com/api"

    def __init__(self, auth_token: str, company_id: str) -> None:
        self.client = httpx.Client(http2=True)
        self.client.auth = (auth_token, "")
        self.company_id = company_id

    def __del__(self) -> None:
        self.client.close()

    def get_branches(self) -> Optional[list]:
        url = f"{self.url}/company/get_branches"
        try:
            response = self.client.post(url, json={"company_id": self.company_id})
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        return response.text
