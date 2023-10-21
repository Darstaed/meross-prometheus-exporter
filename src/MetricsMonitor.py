from prometheus_client import Gauge

from ConnectionManager import ConnectionManager
from MonitorCache import MonitorCache
from Logger import Logger

num_devices = Gauge("meross_metricsmonitor_devices", "Number of devices being monitored.")
monitor_consumption= Gauge("meross_monitor_consumption", "Power consumption (W)", ["id", "name", "type"])

class MetricsMonitor:
    _connections: ConnectionManager
    _monitor_cache: MonitorCache
    _logger: Logger

    def __init__(self, logger: Logger, connections: ConnectionManager, monitor_cache: MonitorCache) -> None:
        self._logger = logger
        self._connections = connections
        self._monitor_cache = monitor_cache

    async def update_metrics(self):
        manager = await self._connections.get_meross_manager()

        await manager.async_device_discovery()
        found_monitors = manager.find_devices(device_type="mss310")
        self._logger.info("Device discovery complete.")
        num_devices.set_function(lambda: len(found_monitors))

        for found_monitor in found_monitors:
            self._logger.debug("Processing device " + found_monitor.uuid)
            monitor = await self._monitor_cache.get_monitor(found_monitor)
            guage = monitor_consumption.labels(monitor.uuid, monitor.name, monitor.type)

            metrics =  await monitor.async_get_instant_metrics()
            self._logger.debug(f"Retrieved metrics: {metrics}")
            guage.set(metrics.power)