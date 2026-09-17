from __future__ import annotations

from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID
from .coordinator import WindFreeCoordinator


class SamsungWindFreeEntity(CoordinatorEntity[WindFreeCoordinator]):
    """Base entity attached to the existing SmartThings A/C device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WindFreeCoordinator, entry) -> None:
        super().__init__(coordinator)
        self._device_id = entry.data[CONF_DEVICE_ID]

    @property
    def device_info(self):
        """Do not create a second Samsung WindFree device.

        The entity is linked to the existing SmartThings device in
        async_added_to_hass instead.
        """
        return None

    async def async_added_to_hass(self) -> None:
        """Attach this entity to the existing SmartThings A/C card."""
        await super().async_added_to_hass()

        device_registry = dr.async_get(self.hass)
        entity_registry = er.async_get(self.hass)

        # Home Assistant SmartThings creates the climate component as a child
        # device using <SmartThings device id>_<component>. For Samsung A/C the
        # main climate component is normally "main".
        target = dr.async_get_device(
            device_registry,
            identifiers={('smartthings', f'{self._device_id}_main')},
        )

        # Fallback to the SmartThings parent device if HA did not create a
        # separate main-component device.
        if target is None:
            target = dr.async_get_device(
                device_registry,
                identifiers={('smartthings', self._device_id)},
            )

        if target is None or self.entity_id is None:
            return

        registry_entry = entity_registry.async_get(self.entity_id)
        if registry_entry is not None and registry_entry.device_id != target.id:
            entity_registry.async_update_entity(
                self.entity_id,
                device_id=target.id,
            )
