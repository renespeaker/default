"""Sensor platform for the Example Integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ExampleConfigEntry
from .const import DOMAIN
from .coordinator import ExampleDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ExampleConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([ExampleSensor(coordinator, entry)])


class ExampleSensor(CoordinatorEntity[ExampleDataUpdateCoordinator], SensorEntity):
    """Representation of an example sensor."""

    _attr_has_entity_name = True
    _attr_name = "Value"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "units"

    def __init__(
        self,
        coordinator: ExampleDataUpdateCoordinator,
        entry: ExampleConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_value"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Example",
        }

    @property
    def native_value(self) -> float | None:
        """Return the current value reported by the coordinator."""
        return self.coordinator.data.get("value")
