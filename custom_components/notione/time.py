"""Time entities (theft alarm hours) for notiOne GPS."""
from __future__ import annotations

from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity

# (translation key, config field, icon)
TIMES = (
    ("theft_alarm_begin", "theftAlarmBeginTime", "mdi:clock-start"),
    ("theft_alarm_end", "theftAlarmEndTime", "mdi:clock-end"),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(
        AlarmTime(c, did, key, field, icon)
        for did in c.data
        if did in c.configs
        for key, field, icon in TIMES
        if field in c.configs[did]
    )


class AlarmTime(NotiOneEntity, TimeEntity):
    """Used by the app when "all day" is off."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, c, did, key: str, field: str, icon: str) -> None:
        super().__init__(c, did, key)
        self._field = field
        self._attr_icon = icon

    @property
    def native_value(self) -> time | None:
        value = self.config.get(self._field)
        try:
            return time.fromisoformat(value) if value else None
        except ValueError:
            return None

    async def async_set_value(self, value: time) -> None:
        await self.coordinator.async_set_config(
            self.device_id, **{self._field: value.replace(microsecond=0).strftime("%H:%M:%S")}
        )
