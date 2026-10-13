"""Data coordinator for notiOne GPS."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NotiOneApi, NotiOneApiError, NotiOneAuthError
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, EVENT_ACCELEROMETER

_LOGGER = logging.getLogger(__name__)

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

        # Never poll more often than the server's own refresh interval.
        server = max((int(d.get("refreshIntervalSeconds") or 0) for d in devices.values()), default=0)
        interval = timedelta(seconds=max(self._configured_interval, server))
        if interval != self.update_interval:
            _LOGGER.debug("Polling interval set to %s", interval)
            self.update_interval = interval
        return devices
