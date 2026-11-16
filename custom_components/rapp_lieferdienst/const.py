"""Constants for the Rapp Lieferdienst integration."""
from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "rapp_lieferdienst"
CONF_CUSTOMER_ID = "customer_id"
API_URL_FORMAT = "https://brauerei-rapp.de/api/calendar?kdnr={}"
PLATFORMS = [Platform.CALENDAR, Platform.SENSOR]
UPDATE_INTERVAL = timedelta(hours=6)
REQUEST_TIMEOUT = 15
