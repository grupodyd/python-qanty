# -*- coding: UTF-8 -*-
import logging
from typing import Union

import httpx

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Qanty:
    url = "https://qanty.com/api"

    def __init__(self, auth_token) -> None:
        self.client = httpx.Client(http2=True)
        self.client.auth = (auth_token, "")

    def __del__(self) -> None:
        self.client.close()


    def get_branches(self, company_id: str) -> Union[list, None]:
        url = f"{self.url}/company/get_branches"
        try:
            response = self.client.post(url, json={"company_id": company_id})
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        return response.text
