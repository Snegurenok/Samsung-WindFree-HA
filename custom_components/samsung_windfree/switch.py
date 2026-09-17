from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import SamsungWindFreeEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SamsungWindFreeSwitch(coordinator, entry)])


class SamsungWindFreeSwitch(SamsungWindFreeEntity, SwitchEntity):
    _attr_name = "WindFree"
    _attr_icon = "mdi:weather-windy"

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{self._device_id}_windfree"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data in ("windFree", "windFreeSleep")

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.api.set_optional_mode("windFree")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.api.set_optional_mode("off")
        await self.coordinator.async_request_refresh()
