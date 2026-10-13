"""Binary sensors for notiOne GPS."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import STATIONARY
from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    entities = []
    for did in c.data:
        entities += [Motion(c, did), Online(c, did), Charging(c, did)]
    async_add_entities(entities)


class Motion(NotiOneEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.MOTION

    def __init__(self, c, did):
        super().__init__(c, did, "motion")

    @property
    def is_on(self) -> bool | None:
        accel = self.position.get("accelerometerStatusEnum")
        speed = self.position.get("speed") or 0
        if accel is None and not speed:
            return None
        return bool((accel and accel != STATIONARY) or speed > 0)

    @property
    def extra_state_attributes(self):
        return {"accelerometer": self.position.get("accelerometerStatusEnum")}


class Online(NotiOneEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, c, did):
        super().__init__(c, did, "online")

    @property
    def is_on(self) -> bool:
        return self.device.get("deviceState") == "ONLINE"


class Charging(NotiOneEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    def __init__(self, c, did):
        super().__init__(c, did, "charging")

    @property
    def is_on(self) -> bool | None:
        return self.gps.get("akuCharging")
