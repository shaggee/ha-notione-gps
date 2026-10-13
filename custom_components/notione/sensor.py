"""Sensors for notiOne GPS."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from .coordinator import NotiOneConfigEntry
from .entity import NotiOneEntity


def _ms(v: Any) -> datetime | None:
    return datetime.fromtimestamp(v / 1000, tz=timezone.utc) if v else None


def _iso(v: Any) -> datetime | None:
    return dt_util.parse_datetime(v) if v else None


def _sub(d: dict) -> dict:
    return d.get("subscription") or {}


@dataclass(frozen=True, kw_only=True)
class NotiOneSensorDescription(SensorEntityDescription):
    value_fn: Callable[[dict, dict, dict], Any]  # (position, gpsDetails, device)


SENSORS: tuple[NotiOneSensorDescription, ...] = (
    NotiOneSensorDescription(
        key="accelerometer", icon="mdi:vibrate",
        value_fn=lambda p, g, d: p.get("accelerometerStatusEnum"),
    ),
    NotiOneSensorDescription(
        key="battery", device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda p, g, d: g.get("battery"),
    ),
    NotiOneSensorDescription(
        key="temperature", device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda p, g, d: p.get("temperature"),
    ),
    NotiOneSensorDescription(
        key="humidity", device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE, state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda p, g, d: p.get("humidity"),
    ),
    NotiOneSensorDescription(
        key="speed", device_class=SensorDeviceClass.SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda p, g, d: p.get("speed"),
    ),
    NotiOneSensorDescription(
        key="last_report", device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda p, g, d: _ms(p.get("gpstime")),
    ),
    NotiOneSensorDescription(
        key="place", icon="mdi:map-marker",
        value_fn=lambda p, g, d: ", ".join(
            x for x in (p.get("geocodePlace"), p.get("geocodeCity")) if x
        ) or None,
    ),
    NotiOneSensorDescription(
        key="orientation", icon="mdi:axis-arrow", entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda p, g, d: p.get("gpsOrientationEnum"),
    ),
    NotiOneSensorDescription(
        key="gps_snr", icon="mdi:satellite-variant", entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT, entity_registry_enabled_default=False,
        value_fn=lambda p, g, d: p.get("gpsSnr"),
    ),
    NotiOneSensorDescription(
        key="last_button", device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda p, g, d: _iso(g.get("lastButtonPressTime")),
    ),
    NotiOneSensorDescription(
        key="last_paired", device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda p, g, d: _iso(d.get("lastPairedTime")),
    ),
    NotiOneSensorDescription(
        key="imei", icon="mdi:sim", entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda p, g, d: str(g["imei"]) if g.get("imei") else None,
    ),
    NotiOneSensorDescription(
        key="subscription", icon="mdi:card-account-details",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda p, g, d: _sub(d).get("subscriptionType"),
    ),
    NotiOneSensorDescription(
        key="subscription_end", device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda p, g, d: _iso(_sub(d).get("endDate")),
    ),
    NotiOneSensorDescription(
        key="refresh_interval", device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda p, g, d: d.get("refreshIntervalSeconds"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: NotiOneConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    c = entry.runtime_data
    async_add_entities(NotiOneSensor(c, did, d) for did in c.data for d in SENSORS)


class NotiOneSensor(NotiOneEntity, SensorEntity):
    entity_description: NotiOneSensorDescription

    def __init__(self, c, did, description: NotiOneSensorDescription) -> None:
        super().__init__(c, did, description.key)
        self.entity_description = description

    @property
    def native_value(self):
        return self.entity_description.value_fn(self.position, self.gps, self.device)
