"""Config flow for Rapp Lieferdienst."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RappApiClient, RappApiError
from .const import CONF_CUSTOMER_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_CUSTOMER_ID): str})


class RappLieferdienstConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Rapp Lieferdienst."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            customer_id = user_input[CONF_CUSTOMER_ID]
            session = async_get_clientsession(self.hass)
            api_client = RappApiClient(customer_id, session)

            try:
                await api_client.async_get_events()
            except RappApiError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(customer_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Rapp Lieferkalender ({customer_id})", data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "OptionsFlowHandler":
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow."""

    # FEHLERHAFTE __init__ METHODE WURDE ENTFERNT
    # Die `self.config_entry` wird von der Basisklasse bereitgestellt
    # und darf hier nicht überschrieben werden.

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            session = async_get_clientsession(self.hass)
            api_client = RappApiClient(user_input[CONF_CUSTOMER_ID], session)
            try:
                await api_client.async_get_events()
            except RappApiError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=user_input
                )
                # Nach dem Update den Flow beenden
                return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_CUSTOMER_ID,
                        default=self.config_entry.data.get(CONF_CUSTOMER_ID),
                    ): str
                }
            ),
            errors=errors,
        )
