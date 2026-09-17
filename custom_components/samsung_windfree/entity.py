from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, CONF_DEVICE_NAME, DOMAIN
from .coordinator import WindFreeCoordinator


class SamsungWindFreeEntity(CoordinatorEntity[WindFreeCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WindFreeCoordinator, entry) -> None:
        super().__init__(coordinator)
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._device_name = entry.data[CONF_DEVICE_NAME]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self._device_name,
            manufacturer="Samsung Electronics",
            model="SmartThings Air Conditioner",
        )
