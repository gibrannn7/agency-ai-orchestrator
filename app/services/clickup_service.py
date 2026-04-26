import httpx
from app.core.config import settings
from app.core.logger import logger
from typing import List, Dict, Any, Optional
import asyncio

class ClickUpService:
    def __init__(self):
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": settings.CLICKUP_API_TOKEN,
            "Content-Type": "application/json"
        }
        self.team_id = settings.CLICKUP_TEAM_ID

    async def get_spaces(self) -> List[Dict[str, Any]]:
        """Fetch spaces for the team."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/team/{self.team_id}/space",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("spaces", [])
            except Exception as e:
                logger.error(f"ClickUp get_spaces Error: {str(e)}")
                raise

    async def create_folder(self, space_id: str, name: str) -> Dict[str, Any]:
        """Create a folder in ClickUp."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/space/{space_id}/folder",
                    headers=self.headers,
                    json={"name": name}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"ClickUp create_folder Error: {str(e)}")
                raise

    async def create_list(self, folder_id: str, name: str) -> Dict[str, Any]:
        """Create a list inside a folder."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/folder/{folder_id}/list",
                    headers=self.headers,
                    json={"name": name}
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"ClickUp create_list Error: {str(e)}")
                raise

    async def create_task(self, list_id: str, name: str, description: str) -> Dict[str, Any]:
        """Create a single task."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/list/{list_id}/task",
                    headers=self.headers,
                    json={
                        "name": name,
                        "description": description
                    }
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"ClickUp create_task Error: {str(e)}")
                raise

    async def create_tasks_batch(self, list_id: str, tasks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Create multiple tasks sequentially to avoid rate limits since
        ClickUp v2 API doesn't have a single bulk task creation endpoint.
        """
        created_tasks = []
        for task in tasks:
            result = await self.create_task(list_id, task["name"], task["description"])
            created_tasks.append(result)
            await asyncio.sleep(0.5)  # Rate limit prevention
        return created_tasks

clickup_service = ClickUpService()
