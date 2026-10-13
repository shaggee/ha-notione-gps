"""Number entities (alarm thresholds) for notiOne GPS."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfSpeed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity

# (translation key, config field, min, max, step, unit, icon)
NUMBERS = (
    ("speed_alarm_threshold", "speedExceedAlarmThreshold", 10, 250, 5,
     UnitOfSpeed.KILOMETERS_PER_HOUR, "mdi:speedometer"),
    ("battery_saving_threshold", "batterySavingAlarmThreshold", 5, 100, 5,
     PERCENTAGE, "mdi:battery-alert-variant-outline"),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(
        ConfigNumber(c, did, *spec)
        for did in c.data
        if did in c.configs
        for spec in NUMBERS
        if spec[1] in c.configs[did]
    )


class ConfigNumber(NotiOneEntity, NumberEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX

    def __init__(self, c, did, key, field, vmin, vmax, step, unit, icon) -> None:
        super().__init__(c, did, key)
        self._field = field
        self._attr_native_min_value = vmin
        self._attr_native_max_value = vmax
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

    @property
    def native_value(self) -> float | None:
        return self.config.get(self._field)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_config(self.device_id, **{self._field: int(value)})
