import logging

from rich.logging import RichHandler
from rich.console import Console


logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("chanty")
console = Console()


def info(text: str):
    log.info(text, extra={"markup": True})


def success(text: str):
    log.info(f'[green]{text}[/green]', extra={"markup": True})


def error(text: str):
    log.error(f'[bold][red]{text}[/red][/bold]', extra={"markup": True})
