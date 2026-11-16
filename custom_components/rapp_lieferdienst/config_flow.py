"""Config flow for Rapp Lieferdienst."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RappApiClient, RappApiError
from .const import CONF_CUSTOMER_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)


def _schema(default: str | None = None) -> vol.Schema:
    """Return the form schema, optionally pre-filled."""
    key = (
        vol.Required(CONF_CUSTOMER_ID, default=default)
        if default
        else vol.Required(CONF_CUSTOMER_ID)
    )
    return vol.Schema({key: str})


async def _async_validate(hass: HomeAssistant, customer_id: str) -> str | None:
    """Try to fetch the calendar. Return an error key or None on success."""
    try:
        await RappApiClient(customer_id, async_get_clientsession(hass)).async_get_events()
    except RappApiError:
        return "cannot_connect"
    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("Unexpected exception")
        return "unknown"
    return None


class RappLieferdienstConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Rapp Lieferdienst."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            customer_id = user_input[CONF_CUSTOMER_ID].strip()
            await self.async_set_unique_id(customer_id)
            self._abort_if_unique_id_configured()
            if not (error := await _async_validate(self.hass, customer_id)):
                return self.async_create_entry(
                    title=f"Rapp Lieferkalender ({customer_id})",
                    data={CONF_CUSTOMER_ID: customer_id},
                )
            errors["base"] = error

        return self.async_show_form(
            step_id="user", data_schema=_schema(), errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Allow changing the customer number via "Neu konfigurieren"."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        if user_input is not None:
            customer_id = user_input[CONF_CUSTOMER_ID].strip()
            if not (error := await _async_validate(self.hass, customer_id)):
                return self.async_update_reload_and_abort(
                    entry,
                    title=f"Rapp Lieferkalender ({customer_id})",
                    data={CONF_CUSTOMER_ID: customer_id},
                )
            errors["base"] = error

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_schema(entry.data.get(CONF_CUSTOMER_ID)),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        # HA sets self.config_entry itself; passing it to __init__ caused the
        # "Config flow could not be loaded: 500" error.
        return OptionsFlowHandler()


class OptionsFlowHandler(OptionsFlow):
    """Options flow (gear icon): change the customer number."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            customer_id = user_input[CONF_CUSTOMER_ID].strip()
            if not (error := await _async_validate(self.hass, customer_id)):
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    title=f"Rapp Lieferkalender ({customer_id})",
                    data={CONF_CUSTOMER_ID: customer_id},
                )
                # Returning an entry triggers the update listener -> reload.
                return self.async_create_entry(data={})
            errors["base"] = error

        return self.async_show_form(
            step_id="init",
            data_schema=_schema(self.config_entry.data.get(CONF_CUSTOMER_ID)),
            errors=errors,
        )
