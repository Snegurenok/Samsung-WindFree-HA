from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SmartThingsWindFreeApi

_LOGGER = logging.getLogger(__name__)


class WindFreeCoordinator(DataUpdateCoordinator[str | None]):
    def __init__(self, hass: HomeAssistant, api: SmartThingsWindFreeApi) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Samsung WindFree",
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    async def _async_update_data(self) -> str | None:
        try:
            return await self.api.get_optional_mode()
        except Exception as err:
            raise UpdateFailed(f"SmartThings status request failed: {err}") from err
