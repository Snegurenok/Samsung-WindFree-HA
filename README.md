# Samsung WindFree for Home Assistant

Custom integration exposing Samsung SmartThings `custom.airConditionerOptionalMode` in Home Assistant.

Supported optional modes for the target Samsung A/C include `off`, `sleep`, `quiet`, `smart`, `speed`, `windFree`, and `windFreeSleep` when reported by the device.

## HACS installation

1. In HACS open Integrations > three-dot menu > Custom repositories.
2. Add this GitHub repository URL and select category **Integration**.
3. Install **Samsung WindFree**.
4. Restart Home Assistant.
5. Go to Settings > Devices & services > Add integration > Samsung WindFree.

## Configuration

The integration requires a SmartThings Personal Access Token with permission to read and control devices and the SmartThings Device ID of the Samsung air conditioner.
