from __future__ import annotations

from typing import Any
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SmartThingsWindFreeApi
from .const import CONF_DEVICE_ID, CONF_DEVICE_NAME, CONF_TOKEN, DOMAIN


class SamsungWindFreeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            token = user_input[CONF_TOKEN].strip()
            device_id = user_input[CONF_DEVICE_ID].strip()
            api = SmartThingsWindFreeApi(async_get_clientsession(self.hass), token, device_id)
            try:
                device = await api.get_device()
                await api.get_status()
            except aiohttp.ClientResponseError as err:
                errors["base"] = "invalid_auth" if err.status in (401, 403) else "cannot_connect"
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(device_id)
                self._abort_if_unique_id_configured()
                name = device.get("label") or device.get("name") or "Samsung Air Conditioner"
                return self.async_create_entry(
                    title=name,
                    data={CONF_TOKEN: token, CONF_DEVICE_ID: device_id, CONF_DEVICE_NAME: name},
                )

        schema = vol.Schema({
            vol.Required(CONF_TOKEN): str,
            vol.Required(CONF_DEVICE_ID): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
