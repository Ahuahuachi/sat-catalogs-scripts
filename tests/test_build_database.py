""" Test build_database function. """

import os

import click
import pytest
from click.testing import CliRunner

from src.sat_catalogs.cli import cli

runner = CliRunner()


class TestBuildDatabase:
    """Build database tests."""

    def test_build_database(self):
        """
        Test the build-database function.
        """
        db_path = str("test.catalogs.db")
        result = runner.invoke(cli, ["build-database", "--name", db_path])
        os.unlink(db_path)
        assert result.exit_code == 0

    def test_build_database_with_overwrite(self):
        """
        Test the build-database function with --overwrite option.
        """
        db_path = str("test.catalogs.db")
        with open(db_path, "wb"):
            pass
        result = runner.invoke(
            cli, ["build-database", "--name", db_path, "--overwrite"]
        )
        os.unlink(db_path)
        assert result.exit_code == 0
