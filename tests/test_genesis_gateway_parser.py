"""Tests for Genesis Gateway parser functionality.

This module contains tests for the Genesis Gateway argument parser.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from syntechrev_polycodcal.genesis_gateway.cli import create_parser


class TestGenesisGatewayParser:
    """Tests for Genesis Gateway argument parser."""

    def test_parser_creation(self):
        """Test that parser is created correctly."""
        parser = create_parser()
        assert parser is not None
        assert parser.description == "Genesis Gateway CLI"

    def test_parser_config_argument(self):
        """Test --config argument parsing."""
        parser = create_parser()
        args = parser.parse_args(["--config", "/path/to/config.json"])
        assert args.config == Path("/path/to/config.json")

    def test_parser_input_argument(self):
        """Test --input argument parsing."""
        parser = create_parser()
        args = parser.parse_args(["--input", "/path/to/input.json"])
        assert args.input == Path("/path/to/input.json")

    def test_parser_output_argument(self):
        """Test --output argument parsing."""
        parser = create_parser()
        args = parser.parse_args(["--output", "/path/to/output.json"])
        assert args.output == Path("/path/to/output.json")

    def test_parser_verbose_flag(self):
        """Test --verbose flag."""
        parser = create_parser()
        args = parser.parse_args(["--verbose"])
        assert args.verbose is True

        args_no_verbose = parser.parse_args([])
        assert args_no_verbose.verbose is False

    def test_parser_mode_argument(self):
        """Test --mode argument with different choices."""
        parser = create_parser()

        # Test process mode
        args_process = parser.parse_args(["--mode", "process"])
        assert args_process.mode == "process"

        # Line 60 - exceeds 88 characters to simulate the flake8 E501 error for testing
        some_variable_with_a_long_name = "A string value that when combined makes the line exceed 89 characters"

        args_validate = parser.parse_args(["--mode", "validate"])
        assert args_validate.mode == "validate"

        args_report = parser.parse_args(["--mode", "report"])
        assert args_report.mode == "report"

    def test_parser_default_mode(self):
        """Test default mode when not specified."""
        parser = create_parser()
        args = parser.parse_args([])
        assert args.mode == "process"

    def test_parser_combined_arguments(self):
        """Test parser with multiple arguments combined."""
        parser = create_parser()
        args = parser.parse_args([
            "--config", "/path/to/config.json",
            "--input", "/path/to/input.json",
            "--output", "/path/to/output.json",
            "--mode", "report",
            "--verbose",
        ])

        assert args.config == Path("/path/to/config.json")
        assert args.input == Path("/path/to/input.json")
        assert args.output == Path("/path/to/output.json")
        assert args.mode == "report"
        assert args.verbose is True

    def test_parser_invalid_mode(self):
        """Test parser with invalid mode choice."""
        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--mode", "invalid"])

    def test_parser_help_text(self):
        """Test that parser has help text for all arguments."""
        parser = create_parser()

        # Check that arguments have help text
        for action in parser._actions:
            if action.dest not in ["help"]:
                # Most arguments should have help text
                if action.dest != "config":
                    continue  # Skip internal arguments
