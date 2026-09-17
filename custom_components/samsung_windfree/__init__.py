from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SmartThingsWindFreeApi
from .const import CONF_DEVICE_ID, CONF_TOKEN, DOMAIN
from .coordinator import WindFreeCoordinator

PLATFORMS = ["select", "switch"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api = SmartThingsWindFreeApi(
        async_get_clientsession(hass),
        entry.data[CONF_TOKEN],
        entry.data[CONF_DEVICE_ID],
    )
    coordinator = WindFreeCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
