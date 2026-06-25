"""DataUpdateCoordinator for the Example Integration."""

from __future__ import annotations

import logging
import random
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ExampleDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that fetches data from the (example) API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.entry = entry

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch the latest data.

        Replace the body of this method with a real API call. The example
        returns a random value so the integration works out of the box.
        """
        try:
            # Example: a real implementation would call
            #   data = await self._client.async_get_data()
            return {"value": round(random.uniform(0, 100), 2)}
        except Exception as err:  # noqa: BLE001 - example placeholder
            raise UpdateFailed(f"Error communicating with API: {err}") from err
