"""The Example Integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from typing import TypeAlias

from .const import DOMAIN
from .coordinator import ExampleDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

ExampleConfigEntry: TypeAlias = ConfigEntry[ExampleDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Set up Example Integration from a config entry."""
    coordinator = ExampleDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ExampleConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: ExampleConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
