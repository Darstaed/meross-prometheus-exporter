from Logger import Logger


from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager


class ConnectionManager:
    _logger: Logger

    _email: str
    _password: str
    _api_base_url: str

    _http_client: MerossHttpClient = None
    _meross_manager: MerossManager = None

    def __init__(self, logger: Logger, api_base_url: str, email: str, password: str) -> None:
        self._logger = logger
        self._email = email
        self._password = password
        self._api_base_url = api_base_url
        pass

    async def finalize(self):
        if (self._meross_manager):
            self._logger.info("Closing Manger")
            self._meross_manager.close()

        if (self._http_client):
            self._logger.info("Logging out")
            await self._http_client.async_logout()

    async def get_http_client(self) -> MerossHttpClient:
        if (not self._http_client):
            self._logger.info("Creating Http Client")
            self._http_client = await MerossHttpClient.async_from_user_password(
                api_base_url=self._api_base_url,
                email=self._email,
                password=self._password
            )

        self._logger.debug("Returning Http Client")
        return self._http_client

    async def get_meross_manager(self) -> MerossManager:
        if (not self._meross_manager):
            self._logger.info("Creating Meross Manager")
            self._meross_manager = MerossManager(await self.get_http_client())
            await self._meross_manager.async_init()

        self._logger.debug("Returning Meross Manager")
        return self._meross_manager