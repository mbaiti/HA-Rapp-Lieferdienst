"""Sensor platform for Rapp Lieferdienst."""

from __future__ import annotations

from datetime import date

from homeassistant.components.sensor import SensorEntity
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
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RappNextDeliverySensor(coordinator, entry)])


class RappNextDeliverySensor(
    CoordinatorEntity[RappDataUpdateCoordinator], SensorEntity
):

    _attr_has_entity_name = True
    _attr_icon = "mdi:truck-delivery"

    def __init__(
        self, coordinator: RappDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_name = "Nächster Rapp Liefertermin"
        self._attr_unique_id = f"{entry.data['customer_id']}-next_delivery"

    @property
    def native_value(self) -> str | None:
        today = dt_util.now().date()

        if not self.coordinator.data:
            self._attr_extra_state_attributes = {}
            return "Unbekannt"

        future_events = sorted(
            event.start
            for event in self.coordinator.data
            if event.start >= today
        )

        if not future_events:
            self._attr_extra_state_attributes = {}
            return "Keine Termine"

        next_event_date = future_events[0]
        days_to = (next_event_date - today).days

        self._attr_extra_state_attributes = {"date": next_event_date.isoformat()}

        if days_to == 0:
            return "Heute"
        elif days_to == 1:
            return "Morgen"
        else:
            return f"in {days_to} Tagen"
