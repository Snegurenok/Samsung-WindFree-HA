from __future__ import annotations

import aiohttp

from .const import API_BASE, ATTRIBUTE, CAPABILITY, COMMAND


class SmartThingsWindFreeApi:
    def __init__(self, session: aiohttp.ClientSession, token: str, device_id: str) -> None:
        self._session = session
        self._token = token
        self.device_id = device_id

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
        }

    async def get_device(self) -> dict:
        async with self._session.get(
            f"{API_BASE}/devices/{self.device_id}", headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_status(self) -> dict:
        async with self._session.get(
            f"{API_BASE}/devices/{self.device_id}/status", headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def get_optional_mode(self) -> str | None:
        status = await self.get_status()
        return (
            status.get("components", {})
            .get("main", {})
            .get(CAPABILITY, {})
            .get(ATTRIBUTE, {})
            .get("value")
        )

    async def set_optional_mode(self, mode: str) -> None:
        payload = {
            "commands": [{
                "component": "main",
                "capability": CAPABILITY,
                "command": COMMAND,
                "arguments": [mode],
            }]
        }
        async with self._session.post(
            f"{API_BASE}/devices/{self.device_id}/commands",
            headers=self.headers,
            json=payload,
        ) as response:
            response.raise_for_status()
            await response.read()
