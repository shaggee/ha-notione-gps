"""Select entities (report intervals) for notiOne GPS."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity

STATIONARY_INTERVALS = (3600, 21600, 86400)  # values offered by the notiOne app
DEFAULT_MOVE_INTERVALS = (10, 60, 300, 600, 1800, 3600, 10800, 21600, 43200, 86400)


def _label(seconds: int) -> str:
    if seconds % 86400 == 0:
        return f"{seconds // 86400} d"
    if seconds % 3600 == 0:
        return f"{seconds // 3600} h"
    if seconds % 60 == 0:
        return f"{seconds // 60} min"
    return f"{seconds} s"


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    entities = []
    for did in c.data:
        if did in c.configs:
            entities += [
                IntervalSelect(c, did, "move_interval", "movePositionInterval"),
                IntervalSelect(c, did, "stationary_interval", "stationaryPositionInterval"),
            ]
    async_add_entities(entities)


class IntervalSelect(NotiOneEntity, SelectEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:timer-cog-outline"

    def __init__(self, c, did, key: str, field: str) -> None:
        super().__init__(c, did, key)
        self._field = field

    def _values(self) -> list[int]:
        if self._field == "movePositionInterval":
            values = list(self.config.get("allowedMoveIntervals") or DEFAULT_MOVE_INTERVALS)
        else:
            values = list(STATIONARY_INTERVALS)
        current = self.config.get(self._field)
        if isinstance(current, int) and current not in values:
            values = sorted({*values, current})
        return values

    @property
    def options(self) -> list[str]:
        return [_label(v) for v in self._values()]

    @property
    def current_option(self) -> str | None:
        value = self.config.get(self._field)
        return _label(value) if isinstance(value, int) else None

    async def async_select_option(self, option: str) -> None:
        value = {_label(v): v for v in self._values()}[option]
        await self.coordinator.async_set_config(self.device_id, **{self._field: value})
