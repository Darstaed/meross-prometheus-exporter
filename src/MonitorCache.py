from Logger import Logger


class MonitorCache:
    _monitors: dict = dict()
    _logger: Logger

    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    async def get_monitor(self, monitor):
        if not self._monitors.get(monitor.uuid):
            self._logger.debug(f"Initializing monitor {monitor.uuid}({monitor.name})")
            self._monitors[monitor.uuid] = monitor
            await monitor.async_update()

        self._logger.debug(f"Returning monitor {monitor.uuid}")
        return self._monitors[monitor.uuid]