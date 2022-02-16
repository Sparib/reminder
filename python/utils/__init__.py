from typing import Dict, Tuple, Union
import logging
from colorama import init, Fore, Back, Style

init(autoreset=True)


class ColorFormatter(logging.Formatter):
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED + Back.BLACK,
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "CRITICAL": Fore.RED + Back.BLACK + Style.BRIGHT
    }

    RESET = Fore.RESET + Back.RESET + Style.RESET_ALL

    def format(self, record: logging.LogRecord):
        color = self.COLORS.get(record.levelname, "")
        self.formatTime(record)
        if color:
            # record.asctime = Fore.CYAN + record.asctime + self.RESET
            if record.levelname.upper() == "CRITICAL": record.msg = color + record.msg + self.RESET
            record.name = Fore.MAGENTA + str(record.name).ljust(16) + self.RESET
            record.levelname = color + str(record.levelname).ljust(8) + self.RESET
        return logging.Formatter.format(self, record)

    def formatTime(self, record: logging.LogRecord, datefmt=None):
        original = logging.Formatter.formatTime(self, record, datefmt)

        return Fore.CYAN + original + Fore.RESET


class __ColorLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)
        color_formatter = ColorFormatter("%(asctime)s | %(levelname)8s | %(name)16s : %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)


def __main():
    logging.setLoggerClass(__ColorLogger)
    logger = logging.getLogger(__name__)
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.debug("This is a debug message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    __main()

def setup_configs(config: Dict[str, Union[str, None]]) -> Tuple[Dict[str, Union[str, None]], Dict[str, Union[str, None]]]:
    new_config = config.copy()
    trello = {}
    for key in config:
        if not key.startswith("TRELLO_"): continue
        trello[key.replace("TRELLO_", "")] = config[key]
        new_config.pop(key)
    config = new_config
    return config, trello