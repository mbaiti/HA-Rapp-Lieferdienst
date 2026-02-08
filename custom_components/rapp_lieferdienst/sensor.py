"""Sensor platform for Rapp Lieferdienst."""
from __future__ import annotations

from datetime import date

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

    _attr_device_class = SensorDeviceClass.DATE
    _attr_has_entity_name = True

    def __init__(
        self, coordinator: RappDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Nächster Rapp Liefertermin"
        self._attr_unique_id = f"{entry.data['customer_id']}-next_delivery"

    @property
    def native_value(self) -> date | None:
        """Return the next delivery date."""
        today = dt_util.now().date()

        if not self.coordinator.data:
            return None

        future_events = sorted(
            event.start
            for event in self.coordinator.data
            if event.start >= today
        )

        return future_events[0] if future_events else None
