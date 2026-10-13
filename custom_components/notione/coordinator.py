"""Data coordinator for notiOne GPS."""
from __future__ import annotations

from datetime import timedelta
import logging
import time
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NotiOneApi, NotiOneApiError, NotiOneAuthError
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, EVENT_ACCELEROMETER

_LOGGER = logging.getLogger(__name__)

CONFIG_REFRESH = 300  # seconds between device settings reads
MAX_SERVER_FLOOR = 60  # seconds

type NotiOneConfigEntry = ConfigEntry[NotiOneCoordinator]


class NotiOneCoordinator(DataUpdateCoordinator[dict[int, dict[str, Any]]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, api: NotiOneApi) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            ),
        )
        self.api = api
        self._last_accel: dict[int, str | None] = {}
        self._configured_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        self.configs: dict[int, dict[str, Any]] = {}
        self._configs_fetched = 0.0

    async def _async_update_data(self) -> dict[int, dict[str, Any]]:
        try:
            devices = await self.api.devices()
        except NotiOneAuthError as err:
            raise ConfigEntryAuthFailed from err
        except NotiOneApiError as err:
            raise UpdateFailed(str(err)) from err

        for did, dev in devices.items():
            accel = (dev.get("lastPosition") or {}).get("accelerometerStatusEnum")
            if did in self._last_accel and self._last_accel[did] != accel:
                _LOGGER.debug("Device %s accelerometer %s -> %s", did, self._last_accel[did], accel)
                self.hass.bus.async_fire(
                    EVENT_ACCELEROMETER,
                    {"device_id": did, "name": dev.get("name"),
                     "from": self._last_accel[did], "to": accel},
                )
            self._last_accel[did] = accel

        # refreshIntervalSeconds follows the tracker's "moving" report interval.
        # Never poll faster than that, but cap the floor so a long interval
        # (e.g. 1 day) does not stop stationary updates and motion events.
        server = max(
            (int((d.get("gpsDetails") or {}).get("refreshIntervalSeconds") or 0) for d in devices.values()),
            default=0,
        )
        interval = timedelta(seconds=max(self._configured_interval, min(server, MAX_SERVER_FLOOR)))
        if interval != self.update_interval:
            _LOGGER.debug("Polling interval set to %s", interval)
            self.update_interval = interval

        if time.monotonic() - self._configs_fetched > CONFIG_REFRESH or set(devices) - set(self.configs):
            await self._async_fetch_configs(devices)
        return devices

    async def _async_fetch_configs(self, devices) -> None:
        configs: dict[int, dict[str, Any]] = {}
        for did in devices:
            try:
                configs[did] = await self.api.device_config(did)
            except (NotiOneApiError, NotiOneAuthError) as err:
                _LOGGER.debug("Could not read config of %s: %s", did, err)
                if did in self.configs:
                    configs[did] = self.configs[did]
        self.configs = configs
        self._configs_fetched = time.monotonic()

    async def async_set_config(self, device_id: int, **changes: Any) -> None:
        """Change device settings: read fresh config, merge, write, re-read."""
        try:
            current = await self.api.device_config(device_id)
            await self.api.set_device_config(device_id, {**current, **changes})
            self.configs[device_id] = await self.api.device_config(device_id)
        except NotiOneAuthError as err:
            raise ConfigEntryAuthFailed from err
        except NotiOneApiError as err:
            raise HomeAssistantError(f"notiOne: {err}") from err
        self.async_update_listeners()
