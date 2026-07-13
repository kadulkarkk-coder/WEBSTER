import logging
from pathlib import Path
from datetime import datetime


class Logger:
    """
    Professional logging system for AURA.
    """

    _logger = None

    def __init__(self):

        if Logger._logger is None:

            Path("logs").mkdir(exist_ok=True)

            log_name = datetime.now().strftime("%Y-%m-%d") + ".log"

            log_path = Path("logs") / log_name

            logger = logging.getLogger("AURA")

            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S"
            )

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(
                log_path,
                encoding="utf-8"
            )

            file_handler.setFormatter(formatter)

            logger.addHandler(console_handler)

            logger.addHandler(file_handler)

            Logger._logger = logger

        self.logger = Logger._logger

    def debug(self, message):

        self.logger.debug(message)

    def info(self, message):

        self.logger.info(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)

    def critical(self, message):

        self.logger.critical(message)