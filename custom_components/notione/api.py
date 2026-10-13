"""Minimal client for the (unofficial) notiOne panel API."""
from __future__ import annotations

import time
from typing import Any

import aiohttp

from .const import API_URL, AUTH_URL, CLIENT_BASIC

# Phones registered as notiOne beacons (deviceType PHONE / BEACON_PHONE)
# report no position or samples through this API, so they are not exposed.
SKIPPED_DEVICE_TYPES = {"PHONE"}

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://panel.notione.com",
    "Referer": "https://panel.notione.com/",
}


class NotiOneAuthError(Exception):
    """Wrong credentials."""


class NotiOneApiError(Exception):
    """Communication problem."""


class NotiOneApi:
    def __init__(self, session: aiohttp.ClientSession, email: str, password: str) -> None:
        self._session = session
        self._email = email
        self._password = password
        self._token: str | None = None
        self._token_exp = 0.0

    async def login(self) -> None:
        try:
            async with self._session.post(
                AUTH_URL,
                json={"email": self._email, "password": self._password, "scope": "NOTI"},
                headers={**HEADERS, "Authorization": f"Basic {CLIENT_BASIC}"},
                timeout=aiohttp.ClientTimeout(total=20),
            ) as resp:
                if resp.status in (400, 401, 403):
                    raise NotiOneAuthError
                resp.raise_for_status()
                data = await resp.json(content_type=None)
        except NotiOneAuthError:
            raise
        except (aiohttp.ClientError, TimeoutError) as err:
            raise NotiOneApiError(str(err)) from err
        if "accessToken" not in data:
            raise NotiOneAuthError
        self._token = data["accessToken"]
        self._token_exp = time.monotonic() + int(data.get("expiresIn", 3600)) - 120

    async def _get(self, path: str, **params: Any) -> Any:
        if not self._token or time.monotonic() > self._token_exp:
            await self.login()
        for attempt in (1, 2):
            try:
                async with self._session.get(
                    f"{API_URL}/{path}",
                    params=params,
                    headers={**HEADERS, "Authorization": f"Bearer {self._token}"},
                    timeout=aiohttp.ClientTimeout(total=20),
                ) as resp:
                    if resp.status == 401 and attempt == 1:
                        await self.login()
                        continue
                    resp.raise_for_status()
                    return await resp.json(content_type=None)
            except (aiohttp.ClientError, TimeoutError) as err:
                raise NotiOneApiError(str(err)) from err
        raise NotiOneAuthError

    async def devices(self) -> dict[int, dict[str, Any]]:
        data = await self._get("devicelist")
        return {
            d["deviceId"]: d
            for d in data.get("deviceList", [])
            if d.get("deviceType") not in SKIPPED_DEVICE_TYPES
        }
