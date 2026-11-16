"""API Client for the Rapp Lieferdienst."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import date, datetime

from aiohttp import ClientError, ClientSession
from icalendar import Calendar

from .const import API_URL_FORMAT, REQUEST_TIMEOUT

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RappEvent:
    """A dataclass to hold parsed event information."""

    uid: str
    summary: str
    description: str
    start: date


class RappApiError(Exception):
    """Base exception for API errors."""


def _to_date(value: date | datetime) -> date:
    """Normalize DTSTART to a plain date (the API delivers all-day events)."""
    return value.date() if isinstance(value, datetime) else value


def parse_calendar(text: str) -> list[RappEvent]:
    """Parse an iCal string into a sorted list of RappEvents."""
    text = text.lstrip("﻿").lstrip()
    if not text.startswith("BEGIN:VCALENDAR"):
        raise RappApiError("Invalid data from API - is the customer number correct?")

    events: list[RappEvent] = []
    for component in Calendar.from_ical(text).walk("VEVENT"):
        dtstart = component.get("dtstart")
        if dtstart is None:
            continue
        start = _to_date(dtstart.dt)
        events.append(
            RappEvent(
                uid=str(component.get("uid") or f"rapp-{start.isoformat()}"),
                summary=str(component.get("summary") or "Rapp Liefertag"),
                description=str(component.get("description") or ""),
                start=start,
            )
        )
    return sorted(events, key=lambda event: event.start)


class RappApiClient:
    """API client to fetch delivery dates from the Rapp API."""

    def __init__(self, customer_id: str, session: ClientSession) -> None:
        """Initialize the API client."""
        self._session = session
        self._url = API_URL_FORMAT.format(customer_id)

    async def async_get_events(self) -> list[RappEvent]:
        """Fetch and parse the calendar events."""
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                async with self._session.get(self._url) as response:
                    response.raise_for_status()
                    text = await response.text()
        except (ClientError, TimeoutError) as err:
            raise RappApiError(f"Error connecting to Rapp API: {err}") from err

        try:
            return parse_calendar(text)
        except RappApiError:
            raise
        except Exception as err:  # icalendar raises ValueError & co.
            raise RappApiError(f"Error parsing calendar: {err}") from err
