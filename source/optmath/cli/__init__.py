"""CLI wrapper package."""


import importlib.util
import logging
from pathlib import Path
from typing import List

import click
from optmath import __version__
from optmath.common.logconfig import configure_logger

DIR = Path(__file__).parent


def cli(args: List[str]):
    """optmath CLI interface API endpoint."""
    return optmath(args)


@click.group(invoke_without_command=True)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    default=False,
)
@click.option(
    "-d",
    "--debug",
    default=False,
    is_flag=True,
    help="Enable debug mode, implies verbose logging.",
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    is_flag=True,
    help="Enable verbose logging, do not implies debug mode.",
)
def optmath(version: bool, debug: bool, verbose: bool):
    """optmath entry point description."""
    if version:
        print(f"optmath version {__version__}")
        exit(0)
    else:
        configure_logger(debug, verbose)


# automatically add all commands defined in CLI dir
for file in DIR.glob("*.py"):
    if not file.name.startswith("_"):
        module_name = file.name.lstrip().rstrip(".py")
        module_spec = importlib.util.spec_from_file_location(
            module_name, str(file)
        )
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        optmath.add_command(getattr(module, module_name))
