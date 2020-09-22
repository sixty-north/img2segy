import logging
import sys

import click
from click import Path
from exit_codes import ExitCode

from img2segy import api
from .version import __version__

log_levels = tuple(logging._levelToName.values())

@click.group()
@click.option(
    "--verbosity",
    default="WARNING",
    help="The logging level to use.",
    type=click.Choice(log_levels, case_sensitive=True),
)
@click.version_option(version=__version__)
def cli(verbosity):
    logging_level = getattr(logging, verbosity)
    logging.basicConfig(level=logging_level)


@cli.command(name="convert")
@click.argument("image", type=click.Path(exists=True))
@click.option("--config", type=click.Path(exists=True), help="Input configuration TOML file")
@click.option("--segy", type=click.Path(writable=True), help="Output SEG-Y file")
@click.option("--force", is_flag=True)
def convert(image: Path, config, segy, force):
    try:
        api.convert(image, segy, config, force=force)
    except Exception as e:
        click.secho(str(e), fg="red")
        sys.exit(ExitCode.DATA_ERR)
    sys.exit(ExitCode.OK)