from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MODES
from .entity import SamsungWindFreeEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SamsungOptionalModeSelect(coordinator, entry)])


class SamsungOptionalModeSelect(SamsungWindFreeEntity, SelectEntity):
    _attr_name = "Optional mode"
    _attr_icon = "mdi:air-conditioner"
    _attr_options = MODES

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{self._device_id}_optional_mode"

    @property
    def current_option(self) -> str | None:
        return self.coordinator.data

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.api.set_optional_mode(option)
        await self.coordinator.async_request_refresh()
