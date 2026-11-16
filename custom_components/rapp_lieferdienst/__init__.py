"""The Rapp Lieferdienst integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant

from .const import PLATFORMS
from .coordinator import RappConfigEntry, RappDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: RappConfigEntry) -> bool:
    """Set up Rapp Lieferdienst from a config entry."""
    coordinator = RappDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: RappConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: RappConfigEntry) -> None:
    """Reload the entry after the customer number was changed."""
    await hass.config_entries.async_reload(entry.entry_id)
