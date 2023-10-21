import asyncio
from datetime import timedelta
import os
from prometheus_client import start_http_server

from ConnectionManager import ConnectionManager
from ConsoleLogger import ConsoleLogger
from Logger import Logger
from MetricsMonitor import MetricsMonitor
from MonitorCache import MonitorCache

class Configuration:
    email: str
    password: str

    api_base_url: str

    metrics_port: int
    metrics_freq: timedelta

    def __init__(self, logger: Logger, email: str, password: str, api_endpoint: str, metrics_port: str, metrics_freq: str) -> None:
        valid_config = True

        if not email:
            valid_config = False
            logger.error("Email is empty")

        if not password:
            valid_config = False
            logger.error("Password is empty")

        if not metrics_port.isdigit():
            valid_config = False
            logger.error("Metrics port is not a valid digit")

        if not metrics_freq.isdigit():
            valid_config = False
            logger.error("Metrics frequency is not a valid digit")

        if not valid_config:
            logger.error("Invalid Configuration")
            raise ValueError("Invalid Configuration")

        self.email = email
        self.password = password
        self.api_base_url = api_endpoint
        self.metrics_port = int(metrics_port)
        self.metrics_freq = timedelta(seconds=int(metrics_freq))

async def update_metrics(freq: timedelta, metrics_monitor: MetricsMonitor):
    while True:
        logger.info("Updating metrics")
        await metrics_monitor.update_metrics()
        await asyncio.sleep(freq.seconds)

def main(logger: Logger, config: Configuration):   
    
    manager = ConnectionManager(
        logger.create_scope("ConnectionManager"),
        api_base_url=config.api_base_url,
        email=config.email,
        password=config.password,
    )
    monitor_cache = MonitorCache(logger.create_scope("MonitorCache"))
    metrics_monitor = MetricsMonitor(logger.create_scope("MetricsMonitor"), manager, monitor_cache)

    # Windows and python 3.8 requires to set up a specific event_loop_policy.
    #  On Linux and MacOSX this is not necessary.
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.get_event_loop()

    logger.info("Initialization complete, begining monitoring")
    try:
        start_http_server(config.metrics_port)
        loop.run_until_complete(update_metrics(config.metrics_freq, metrics_monitor))
        
    except Exception as e:
        logger.error("Exception occurred. Exiting.")
        logger.error(e)
    except:
        pass
    finally:
        loop.run_until_complete(manager.finalize())

        
        
# CLI Configuration
if __name__ == '__main__':
    level = (os.environ.get('LOG_LEVEL') or "3")
    logger = ConsoleLogger("Adapter", int(level))

    config = Configuration(
        logger,
        email=os.environ.get('MEROSS_EMAIL'),
        password=os.environ.get('MEROSS_PASSWORD'),
        api_endpoint=(os.environ.get('MEROSS_BASE_URL') or "https://iotx-eu.meross.com"),
        metrics_port=(os.environ.get('METRICS_PORT') or "8000"),
        metrics_freq=(os.environ.get('METRICS_FREQ_SECONDS') or "300"),
    )

    main(logger, config)
