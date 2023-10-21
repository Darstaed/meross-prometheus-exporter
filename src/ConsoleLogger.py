from Logger import Logger


class ConsoleLogger(Logger):
    _scope: str
    _log_level: int

    def __init__(self, scope: str, log_level: int) -> None:
        self._scope = scope
        self._log_level = log_level

    def create_scope(self, scope: str):
        return ConsoleLogger(f"{self._scope}.{scope}", self._log_level)

    def __format_message(self, level: str, message: str):
        return f"{level}:{self._scope} - {message}"

    def error(self, message: str):
        if self._log_level <= 0:
            return
        print(self.__format_message("ERROR", message))

    def warn(self, message: str):
        if self._log_level <= 1:
            return
        print(self.__format_message("WARN", message))

    def info(self, message: str):
        if self._log_level <= 2:
            return
        print(self.__format_message("INFO", message))

    def debug(self, message: str):
        if self._log_level <= 3:
            return
        print(self.__format_message("DEBUG", message))