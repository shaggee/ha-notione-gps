"""Device tracker for notiOne GPS."""
from __future__ import annotations

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(NotiOneTracker(c, did) for did in c.data)


class NotiOneTracker(NotiOneEntity, TrackerEntity):
    _attr_name = None  # use device name

    def __init__(self, c, did):
        super().__init__(c, did, "location")

    @property
    def source_type(self) -> SourceType:
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        return self.position.get("latitude")

    @property
    def longitude(self) -> float | None:
        return self.position.get("longitude")

    @property
    def location_accuracy(self) -> float:
        return float(self.position.get("accuracy") or 10)

    @property
    def battery_level(self) -> int | None:
        return self.gps.get("battery")

    @property
    def extra_state_attributes(self):
        p = self.position
        return {
            "place": ", ".join(x for x in (p.get("geocodePlace"), p.get("geocodeCity")) if x),
            "speed": p.get("speed"),
            "gps_snr": p.get("gpsSnr"),
        }
