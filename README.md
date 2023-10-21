# Meross Prometheus Exporter
Exports power consumption from Meross mss310 power switches as prometheus compatible metrics.

Based on [MerossIot python library by albertogeniolia](https://github.com/albertogeniola/MerossIot)

## Usage
```sh
docker run --rm -it \
    -e MEROSS_EMAIL={Your Meross Cloud Email Address} \
    -e MEROSS_PASSWORD={Your Meross Cloud Password} \
    -p 8000:8000 \
    docker.io/darstaed/meross-prometheus-adapter
```
### By default:
- Metrics are is exposed over http on port 8000 at '/'.
- Devices are discovered and scraped every 5 minutes.

### Mandatory parameters
**MEROSS_EMAIL** - Your Meross Cloud Email Address, used to obtain a token to discover devices and scrape consumption.

**MEROSS_PASSWORD** - Your Meross Cloud Password, used to obtain a token to discover devices and scrape consumption.

### Optional parameters
**MEROSS_BASE_URL** - Default https://iotx-eu.meross.com - Https base endpoint to use for API calls. It should be one of “https://iotx-eu.meross.com”, “https://iotx-ap.meross.com” or “https://iotx-us.meross.com”, based on your public IP region.

**METRICS_PORT** - Default 8000 - The port to expose metrics on.

**METRICS_FREQ_SECONDS** - Default 300 - Frequency (in seconds) to discover and scrape meross devices. *note* - Meross does not appear to disclose rate limiting information. Increasing the frequency may result in your Meross account being blocked.

## Resource Requirements
*Mem* ~ 32Mb \
*Cpu* ~ 5m

## Metrics
### meross_metricsmonitor_devices
The number of Meross mss310 devices found.

Type: Gauge

### meross_monitor_consumption{id,name,type}
The last scraped power consumption in watts.

Type: Guage

Labels:
- **id** -  The Meross UUID for the device
- **name** - The custom name for the device
- **type** - The type of device (currently only mss310s are scraped)

## To Do
- Test using a more generic device filter (i.e. `meross_iot.controller.mixins.electricity.ElectricityMixin`)
- Use python built in logging