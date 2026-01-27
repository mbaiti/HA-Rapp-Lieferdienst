"""Calendar platform for Rapp Lieferdienst."""
from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RappDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    coordinator: RappDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RappCalendarEntity(coordinator, entry)], True)


class RappCalendarEntity(CoordinatorEntity[RappDataUpdateCoordinator], CalendarEntity):
    """Representation of a Rapp Lieferdienst calendar."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: RappDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the calendar entity."""
        super().__init__(coordinator)
        self._attr_name = "Rapp Lieferkalender"
        self._attr_unique_id = f"{entry.data['customer_id']}-calendar"
        self._event: CalendarEvent | None = None

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        events = []
        if self.coordinator.data:
            for event in self.coordinator.data:
                event_start = event.begin.date()
                if start_date.date() <= event_start < end_date.date():
                    events.append(
                        CalendarEvent(
                            summary=event.name,
                            start=event_start,
                            end=event_start + timedelta(days=1),
                            description=event.description,
                            uid=event.uid,
                        )
                    )
        return events
