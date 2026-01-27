"""DataUpdateCoordinator for the Rapp Lieferdienst integration."""
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RappApiClient, RappApiError, RappEvent

_LOGGER = logging.getLogger(__name__)


class RappDataUpdateCoordinator(DataUpdateCoordinator[list[RappEvent]]):
    """A coordinator to fetch data from the Rapp API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: RappApiClient,
        update_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        self.api_client = api_client
        super().__init__(
            hass,
            _LOGGER,
            name="Rapp Lieferdienst Sensor",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> list[RappEvent]:
        """Fetch data from the API."""
        try:
            return await self.api_client.async_get_events()
        except RappApiError as e:
            raise UpdateFailed(f"Error communicating with API: {e}") from e
