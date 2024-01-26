import logging

from colorama import Fore, Style

# Create a custom logger
LOGGER = logging.getLogger(__name__)

# Set the logging level (change as needed)
LOGGER.setLevel(logging.DEBUG)

# Create a console handler to print log messages to the console
console_handler = logging.StreamHandler()


# Create a formatter to define the log message format with color
class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.MAGENTA,  # Debug messages (violet)
        logging.INFO: Fore.BLUE,  # Info messages (blue)
        logging.WARNING: Fore.YELLOW,  # Warning messages (yellow)
        logging.ERROR: Fore.RED,  # Error messages (red)
        logging.CRITICAL: Fore.RED + Style.BRIGHT,  # Critical messages (red and bold)
    }

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        color = self.COLORS.get(record.levelno, Fore.RESET)
        return f"{color}{log_message}{Fore.RESET}"


formatter = ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Set the formatter for the console handler
console_handler.setFormatter(formatter)

# Add the console handler to the logger
LOGGER.addHandler(console_handler)
