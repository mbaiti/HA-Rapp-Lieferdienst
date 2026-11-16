"""Sensor platform for Rapp Lieferdienst."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .api import RappEvent
from .coordinator import RappConfigEntry, RappDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RappConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([RappNextDeliverySensor(entry.runtime_data, entry)])


class RappNextDeliverySensor(
    CoordinatorEntity[RappDataUpdateCoordinator], SensorEntity
):
    """Shows the next delivery relative to today ("Heute", "Morgen", ...)."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:truck-delivery"
    _attr_name = "Nächster Rapp Liefertermin"

    def __init__(
        self, coordinator: RappDataUpdateCoordinator, entry: RappConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        # entry.unique_id is the customer number the entry was created with.
        # It stays stable when the number is changed later, so the entity
        # keeps its entity_id and history.
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}-next_delivery"

    async def async_added_to_hass(self) -> None:
        """Recalculate the relative state every night just after midnight.

        The coordinator only polls a few times a day; without this the state
        ("Morgen") would stay stale until the next poll on the delivery day.
        """
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_time_change(
                self.hass, self._async_midnight, hour=0, minute=0, second=5
            )
        )

    @callback
    def _async_midnight(self, _now: datetime) -> None:
        self.async_write_ha_state()

    def _next_event(self) -> RappEvent | None:
        today = dt_util.now().date()
        return next(
            (event for event in self.coordinator.data or [] if event.start >= today),
            None,
        )

    @property
    def native_value(self) -> str | None:
        """Return the relative day of the next delivery."""
        if self.coordinator.data is None:
            return None
        if (event := self._next_event()) is None:
            return "Keine Termine"
        days_to = (event.start - dt_util.now().date()).days
        if days_to == 0:
            return "Heute"
        if days_to == 1:
            return "Morgen"
        return f"in {days_to} Tagen"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the date of the next delivery."""
        if (event := self._next_event()) is None:
            return {}
        return {
            "date": event.start.isoformat(),
            "days_until": (event.start - dt_util.now().date()).days,
        }
