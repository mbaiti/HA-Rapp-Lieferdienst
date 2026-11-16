"""DataUpdateCoordinator for the Rapp Lieferdienst integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RappApiClient, RappApiError, RappEvent
from .const import CONF_CUSTOMER_ID, DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

type RappConfigEntry = ConfigEntry[RappDataUpdateCoordinator]


class RappDataUpdateCoordinator(DataUpdateCoordinator[list[RappEvent]]):
    """A coordinator to fetch data from the Rapp API."""

    config_entry: RappConfigEntry

    def __init__(self, hass: HomeAssistant, entry: RappConfigEntry) -> None:
        """Initialize the coordinator."""
        self.api_client = RappApiClient(
            entry.data[CONF_CUSTOMER_ID], async_get_clientsession(hass)
        )
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> list[RappEvent]:
        """Fetch data from the API."""
        try:
            return await self.api_client.async_get_events()
        except RappApiError as err:
            raise UpdateFailed(str(err)) from err
