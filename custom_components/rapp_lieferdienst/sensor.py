"""Sensor platform for Rapp Lieferdienst."""
from __future__ import annotations

from datetime import date, datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import RappDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RappNextDeliverySensor(coordinator, entry)])


class RappNextDeliverySensor(
    CoordinatorEntity[RappDataUpdateCoordinator], SensorEntity
):
    """Representation of a sensor for the next Rapp delivery date."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_has_entity_name = True

    def __init__(
        self, coordinator: RappDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Nächster Rapp Liefertermin"
        self._attr_unique_id = f"{entry.data['customer_id']}-next_delivery"

    @property
    def native_value(self) -> datetime | None:
        """Return the state of the sensor."""
        today = dt_util.now().date()
        next_event_date: date | None = None

        if self.coordinator.data:
            future_events = sorted(
                [
                    event.begin.date()
                    for event in self.coordinator.data
                    if event.begin.date() >= today
                ]
            )
            if future_events:
                next_event_date = future_events[0]

        if next_event_date:
            return datetime.combine(next_event_date, datetime.min.time())
        return None
