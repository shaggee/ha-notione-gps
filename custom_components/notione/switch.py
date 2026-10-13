"""Switches (device settings) for notiOne GPS."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity

# (translation key, config field, icon)
SWITCHES = (
    ("theft_alarm", "theftAlarmStatus", "mdi:shield-car"),
    ("theft_alarm_sound", "theftAlarmSoundEnabled", "mdi:volume-high"),
    ("speed_alarm", "speedExceedAlarmEnabled", "mdi:speedometer"),
    ("battery_saving", "batterySavingAlarmEnabled", "mdi:battery-heart-variant"),
    ("allow_disable", "allowDisableDevice", "mdi:power"),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(
        ConfigSwitch(c, did, key, field, icon)
        for did in c.data
        if did in c.configs
        for key, field, icon in SWITCHES
        if field in c.configs[did]
    )


class ConfigSwitch(NotiOneEntity, SwitchEntity):
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, c, did, key: str, field: str, icon: str) -> None:
        super().__init__(c, did, key)
        self._field = field
        self._attr_icon = icon

    @property
    def is_on(self) -> bool | None:
        value = self.config.get(self._field)
        return None if value is None else bool(value)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.async_set_config(self.device_id, **{self._field: True})

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_set_config(self.device_id, **{self._field: False})
