"""Base entity for notiOne GPS."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import NotiOneCoordinator


class NotiOneEntity(CoordinatorEntity[NotiOneCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: NotiOneCoordinator, device_id: int, key: str) -> None:
        super().__init__(coordinator)
        self.device_id = device_id
        self._attr_unique_id = f"{device_id}_{key}"
        self._attr_translation_key = key
        dev = self.device
        gd = dev.get("gpsDetails") or {}
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device_id))},
            name=dev.get("name") or f"notiOne {device_id}",
            manufacturer="notiOne",
            model=f"{dev.get('deviceType', 'GPS')} {dev.get('deviceVersion', '')}".strip(),
            sw_version=gd.get("firmwareVersion"),
            serial_number=str(gd.get("serialNumber")) if gd.get("serialNumber") else None,
        )

    @property
    def device(self) -> dict[str, Any]:
        return self.coordinator.data.get(self.device_id, {})

    @property
    def position(self) -> dict[str, Any]:
        return self.device.get("lastPosition") or {}

    @property
    def gps(self) -> dict[str, Any]:
        return self.device.get("gpsDetails") or {}

    @property
    def available(self) -> bool:
        return super().available and self.device_id in self.coordinator.data
