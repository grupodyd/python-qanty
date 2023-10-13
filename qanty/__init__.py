# -*- coding: UTF-8 -*-
import logging
from typing import List, Optional

import httpx

import qanty.common.models as models


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class Qanty:
    __url = "https://qanty.com/api"

    def __init__(self, auth_token: str, company_id: str) -> None:
        headers = {"Authorization": auth_token}
        self.client = httpx.Client(http2=True, headers=headers)
        self.company_id = company_id

    def __del__(self) -> None:
        self.client.close()

    def get_branches(self, filters: Optional[dict] = None, get_deleted: Optional[bool] = False) -> Optional[List[models.Branch]]:
        """
        Retrieves a list of branches for the company associated with this Qanty instance.

        :param filters: A dictionary of filters to apply to the branch list. Optional.
        :param get_deleted: Whether to include deleted branches in the list. Optional.
        :return: A list of Branch objects representing the branches for the company, or None if an error occurred.
        """
        url = f"{self.__url}/company/get_branches"
        try:
            response = self.client.post(url, json={"company_id": self.company_id, "filters": filters, "get_deleted": get_deleted})
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        sites = data.get("sites", [])
        branches: List[models.Branch] = [models.Branch.model_validate(item) for item in sites]
        return branches

    def get_lines(
        self, branch_id: Optional[str] = None, custom_branch_id: Optional[str] = None, get_deleted: Optional[bool] = False
    ) -> Optional[List[models.Line]]:
        """
        Retrieves a list of lines from the specified branch or custom branch.

        Args:
            branch_id (Optional[str]): The ID of the branch to retrieve lines from. Defaults to None.
            custom_branch_id (Optional[str]): The ID of the custom branch to retrieve lines from. Defaults to None.
            get_deleted (Optional[bool]): Whether to include deleted lines in the results. Defaults to False.

        Returns:
            Optional[List[models.Line]]: A list of Line objects representing the retrieved lines, or None if an error occurred.
        """
        url = f"{self.__url}/branches/get_lines"
        try:
            response = self.client.post(
                url,
                json={
                    "company_id": self.company_id,
                    "branch_id": branch_id,
                    "custom_branch_id": custom_branch_id,
                    "get_deleted": get_deleted,
                },
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(exc)
            return None

        lines = data.get("lines", [])
        lines: List[models.Line] = [models.Line.model_validate(item) for item in lines]
        return lines
