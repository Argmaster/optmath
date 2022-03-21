"""CLI entry point."""
import sys

from .cli import cli


def main():
    cli(sys.argv[1:])
