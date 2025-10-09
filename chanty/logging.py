import logging

from rich.logging import RichHandler
from rich.console import Console

from .config import config


logging.basicConfig(
    level="DEBUG" if config.debug else "INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("chanty")
console = Console()


def info(text: str):
    if config.verbose:
        log.info(f'[bright_black]{text}[/bright_black]', extra={"markup": True})


def debug(text: str):
    if config.debug:
        log.debug(f'[yellow]{text}[/yellow]', extra={"markup": True})


def error(text: str):
    log.error(f'[bold][red]{text}[/red][/bold]', extra={"markup": True})
