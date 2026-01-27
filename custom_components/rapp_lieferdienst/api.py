"""API Client for the Rapp Lieferdienst."""
import asyncio
import logging
from dataclasses import dataclass
from datetime import date

import async_timeout
from aiohttp import ClientError, ClientSession
from icalendar import Calendar

from .const import API_URL_FORMAT

_LOGGER = logging.getLogger(__name__)


@dataclass
class RappEvent:
    """A dataclass to hold parsed event information."""
    uid: str
    summary: str
    description: str
    start: date


class RappApiError(Exception):
    """Base exception for API errors."""


class RappApiClient:
    """API client to fetch delivery dates from the Rapp API."""

    def __init__(self, customer_id: str, session: ClientSession) -> None:
        """Initialize the API client."""
        self._customer_id = customer_id
        self._session = session
        self._url = API_URL_FORMAT.format(customer_id)

    async def async_get_events(self) -> list[RappEvent]:
        """Fetch and parse the calendar events."""
        try:
            with async_timeout.timeout(10):
                response = await self._session.get(self._url)
                response.raise_for_status()
                text = await response.text()

                if not text.startswith("BEGIN:VCALENDAR"):
                    _LOGGER.error("Invalid data received from API. Is the customer ID correct?")
                    raise RappApiError("Invalid data from API")

                calendar = Calendar.from_ical(text)
                events = []
                for component in calendar.walk():
                    if component.name == "VEVENT":
                        events.append(
                            RappEvent(
                                uid=str(component.get("uid")),
                                summary=str(component.get("summary")),
                                description=str(component.get("description")),
                                start=component.get("dtstart").dt,
                            )
                        )
                return events

        except (ClientError, asyncio.TimeoutError) as e:
            _LOGGER.error("Error connecting to Rapp API: %s", e)
            raise RappApiError from e
        except Exception as e:
            _LOGGER.error("An unexpected error occurred while parsing calendar: %s", e)
            raise RappApiError from e
