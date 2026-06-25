# Example Integration for Home Assistant

A minimal, HACS-compatible [Home Assistant](https://www.home-assistant.io/)
custom integration scaffold. Use it as a starting point for your own
integration: it ships with a UI config flow, a `DataUpdateCoordinator`,
and an example sensor that works out of the box.

## Features

- ⚙️ **Config flow** — set up entirely from the Home Assistant UI, no YAML.
- 🔁 **DataUpdateCoordinator** — efficient, shared polling for all entities.
- 📈 **Example sensor** — reports a value (replace with your real data source).
- 📦 **HACS-ready** — includes `hacs.json` and the standard repo layout.

## Installation

### HACS (recommended)

1. In HACS, add this repository as a *custom repository* (category: *Integration*).
2. Search for **Example Integration** and install it.
3. Restart Home Assistant.

### Manual

Copy `custom_components/example_integration` into your Home Assistant
`config/custom_components` directory and restart Home Assistant.

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Example Integration** and follow the prompts.

## Making it your own

Rename the domain and update these places:

| What | Where |
| --- | --- |
| Domain (`example_integration`) | folder name + `DOMAIN` in `const.py` + `manifest.json` |
| Display name | `manifest.json`, `strings.json`, `hacs.json` |
| Data fetching | `coordinator.py` → `_async_update_data` |
| Entities | `sensor.py` (add more platforms as needed) |

## License

[MIT](LICENSE)
