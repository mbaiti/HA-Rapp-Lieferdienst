"""Calendar platform for Rapp Lieferdienst."""
from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .api import RappEvent
from .coordinator import RappConfigEntry, RappDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RappConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    async_add_entities([RappCalendarEntity(entry.runtime_data, entry)])


def _to_calendar_event(event: RappEvent) -> CalendarEvent:
    return CalendarEvent(
        summary=event.summary,
        start=event.start,
        end=event.start + timedelta(days=1),
        description=event.description or None,
        uid=event.uid,
    )


class RappCalendarEntity(CoordinatorEntity[RappDataUpdateCoordinator], CalendarEntity):
    """Representation of a Rapp Lieferdienst calendar."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:truck-delivery"
    _attr_name = "Rapp Lieferkalender"

    def __init__(
        self, coordinator: RappDataUpdateCoordinator, entry: RappConfigEntry
    ) -> None:
        """Initialize the calendar entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}-calendar"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the current or next upcoming delivery.

        HA derives the entity state (on during a delivery day) from this and
        schedules state updates at the event's start/end itself.
        """
        today = dt_util.now().date()
        for event in self.coordinator.data or []:
            if event.start >= today:
                return _to_calendar_event(event)
        return None

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        return [
            _to_calendar_event(event)
            for event in self.coordinator.data or []
            # an all-day event covers [local midnight, next local midnight)
            if dt_util.start_of_local_day(event.start) < end_date
            and dt_util.start_of_local_day(event.start + timedelta(days=1)) > start_date
        ]
