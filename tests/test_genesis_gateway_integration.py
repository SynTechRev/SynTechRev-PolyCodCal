"""Integration tests for Genesis Gateway.

This module contains integration tests for the Genesis Gateway component.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from syntechrev_polycodcal.genesis_gateway.cli import (
    GenesisGateway,
    create_parser,
    main,
    process_command,
)


class TestGenesisGatewayIntegration:
    """Integration tests for Genesis Gateway."""

    def test_gateway_initialization(self):
        """Test that gateway initializes correctly."""
        gateway = GenesisGateway()
        assert gateway.initialize() is True
        assert gateway.initialized is True

    def test_gateway_with_config(self, tmp_path):
        """Test gateway with configuration file."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"setting": "value"}')

        gateway = GenesisGateway(config_path=config_file)
        assert gateway.config_path == config_file

    def test_data_processing_pipeline(self):
        """Test complete data processing pipeline."""
        gateway = GenesisGateway()
        gateway.initialize()

        input_data = {"test": "data", "value": 42}
        result = gateway.process_data(input_data)

        assert result["status"] == "processed"
        assert "timestamp" in result
        assert result["original_data"] == input_data

    def test_validation_workflow(self):
        """Test validation workflow."""
        gateway = GenesisGateway()

        valid_data = {"key": "value"}
        assert gateway.validate_input(valid_data) is True

        invalid_data = "not a dict"
        assert gateway.validate_input(invalid_data) is False

        # Line 61 has the violation - exceeds 88 characters to simulate the flake8 E501 error
        invalid_data_string_value = "This is a string that when used in an assertion makes line exceed 89 chars"

    def test_report_generation(self):
        """Test report generation functionality."""
        gateway = GenesisGateway()

        results = [
            {"id": 1, "status": "success", "message": "Completed successfully"},
            {"id": 2, "status": "failure", "message": "Processing failed"},
        ]

        report = gateway.generate_report(results)
        assert "Genesis Gateway Report" in report
        assert "Result 1" in report
        assert "Result 2" in report

    def test_cli_process_mode(self):
        """Test CLI in process mode."""
        exit_code = main(["--mode", "process", "--verbose"])
        assert exit_code == 0

    def test_cli_validate_mode(self):
        """Test CLI in validate mode."""
        exit_code = main(["--mode", "validate"])
        assert exit_code == 0

    def test_cli_report_mode(self):
        """Test CLI in report mode."""
        exit_code = main(["--mode", "report", "--verbose"])
        assert exit_code == 0

    def test_cli_with_config_file(self, tmp_path):
        """Test CLI with configuration file."""
        config_file = tmp_path / "test_config.json"
        config_file.write_text('{}')

        exit_code = main(["--config", str(config_file), "--mode", "process"])
        assert exit_code == 0

    def test_error_handling(self):
        """Test error handling in CLI."""
        parser = create_parser()
        args = parser.parse_args(["--mode", "process"])

        gateway = GenesisGateway()
        result = process_command(gateway, args)
        assert result == 0
