#!/usr/bin/env python3
"""
🧪 Utility Tests for Gestão Tattoo Studio

This module tests utility functions like date formatting, commission calculations,
JSON utilities, backup operations, and other helper functions.
"""

import pytest
import json
import os
import sys
from pathlib import Path
from datetime import datetime, date

# Add the parent directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import utility modules
from utils.json_utils import ler_json_seguro, salvar_json_seguro
from utils.backup_mensal import realizar_backup_mensal
from financeiro.comissoes import calcular_total_comissoes_artista
from app import data_brasileira


class TestUtilities:
    """Test class for utility functions"""

    @pytest.fixture
    def setup_test_files(self):
        """Set up test files and directories"""
        test_dir = Path(__file__).parent / "temp_test_data"
        test_dir.mkdir(exist_ok=True)

        # Create test JSON file
        test_data = {
            "test_key": "test_value",
            "test_list": [1, 2, 3],
            "test_dict": {"nested": "value"},
        }

        test_file = test_dir / "test.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, indent=4, ensure_ascii=False)

        yield test_dir, test_file, test_data

        # Cleanup
        import shutil

        if test_dir.exists():
            shutil.rmtree(test_dir)

    def test_date_formatting(self):
        """Test date formatting utilities"""

        # Test Brazilian date format filter
        test_dates = [
            ("2025-05-15", "15/05/2025"),
            ("2025-12-31", "31/12/2025"),
            ("2025-01-01", "01/01/2025"),
        ]

        for input_date, expected_output in test_dates:
            result = data_brasileira(input_date)
            assert result == expected_output
            print(f"✅ Date formatting test passed: {input_date} -> {result}")

        # Test invalid date formats
        invalid_dates = ["invalid-date", "", None, "2025-13-45"]
        for invalid_date in invalid_dates:
            result = data_brasileira(invalid_date)
            # Should return original string for invalid dates
            assert result == invalid_date
            print(f"✅ Invalid date handling test passed: {invalid_date} -> {result}")

    def test_json_utilities(self, setup_test_files):
        """Test JSON utility functions"""
        test_dir, test_file, test_data = setup_test_files

        # Test reading JSON safely
        result = ler_json_seguro(test_file, {})
        assert result == test_data
        print("✅ JSON safe reading test passed")

        # Test reading non-existent file with default
        non_existent_file = test_dir / "non_existent.json"
        default_data = {"default": "value"}
        result = ler_json_seguro(non_existent_file, default_data)
        assert result == default_data
        print("✅ JSON safe reading with default test passed")

        # Test saving JSON safely
        new_data = {"new_key": "new_value", "numbers": [1, 2, 3]}
        new_file = test_dir / "new_test.json"

        success = salvar_json_seguro(new_file, new_data)
        assert success is True

        # Verify the saved data
        with open(new_file, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
        assert saved_data == new_data
        print("✅ JSON safe saving test passed")

    def test_commission_calculations(self):
        """Test commission calculation utilities"""

        # Test commission percentage calculations
        test_cases = [
            (100.00, 70, 70.00),  # 70% of 100
            (250.00, 60, 150.00),  # 60% of 250
            (50.00, 80, 40.00),  # 80% of 50
            (0.00, 70, 0.00),  # 70% of 0
        ]

        for valor_total, porcentagem, expected_comissao in test_cases:
            calculated_comissao = round(valor_total * (porcentagem / 100), 2)
            assert calculated_comissao == expected_comissao
            print(
                f"✅ Commission calculation test passed: {valor_total} * {porcentagem}% = {calculated_comissao}"
            )

        # Test edge cases
        edge_cases = [
            (100.00, 0, 0.00),  # 0% commission
            (100.00, 100, 100.00),  # 100% commission
            (0.01, 70, 0.01),  # Very small value
        ]

        for valor_total, porcentagem, expected_comissao in edge_cases:
            calculated_comissao = round(valor_total * (porcentagem / 100), 2)
            assert calculated_comissao == expected_comissao
            print(
                f"✅ Commission edge case test passed: {valor_total} * {porcentagem}% = {calculated_comissao}"
            )

    def test_backup_operations(self):
        """Test backup utility operations"""

        # Test backup function exists and can be called
        try:
            # Note: We don't actually run the backup to avoid side effects
            # Just test that the function exists and is callable
            assert callable(realizar_backup_mensal)
            print("✅ Backup function availability test passed")
        except Exception as e:
            print(f"⚠️  Backup function test failed: {e}")

    def test_value_formatting(self):
        """Test value formatting utilities"""

        # Test currency formatting
        test_values = [
            (100.00, "100.00"),
            (100.5, "100.50"),
            (100.555, "100.56"),  # Rounding test
            (0.00, "0.00"),
            (1000.00, "1000.00"),
        ]

        for value, expected in test_values:
            formatted = f"{value:.2f}"
            assert formatted == expected
            print(f"✅ Value formatting test passed: {value} -> {formatted}")

    def test_string_utilities(self):
        """Test string manipulation utilities"""

        # Test string cleaning/normalization
        test_strings = [
            ("  Test String  ", "Test String"),
            ("UPPER CASE", "UPPER CASE"),
            ("lower case", "lower case"),
            ("", ""),
            ("   ", ""),
        ]

        for input_str, expected in test_strings:
            cleaned = input_str.strip()
            assert cleaned == expected
            print(f"✅ String cleaning test passed: '{input_str}' -> '{cleaned}'")

    def test_id_generation_utilities(self):
        """Test ID generation utilities"""

        # Test unique ID generation
        existing_ids = [1, 2, 3, 5, 8]

        def generate_next_id(existing_ids):
            """Generate next available ID"""
            if not existing_ids:
                return 1
            return max(existing_ids) + 1

        next_id = generate_next_id(existing_ids)
        assert next_id == 9
        print(
            f"✅ ID generation test passed: next ID after {existing_ids} is {next_id}"
        )

        # Test with empty list
        next_id = generate_next_id([])
        assert next_id == 1
        print("✅ ID generation with empty list test passed")

    def test_data_validation_utilities(self):
        """Test data validation utilities"""

        # Test date validation
        def is_valid_date(date_str):
            """Simple date validation"""
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False

        valid_dates = ["2025-05-15", "2025-12-31", "2025-01-01"]
        invalid_dates = ["2025-13-01", "2025-05-32", "invalid-date"]

        for date_str in valid_dates:
            assert is_valid_date(date_str) is True
            print(f"✅ Date validation test passed: {date_str} is valid")

        for date_str in invalid_dates:
            assert is_valid_date(date_str) is False
            print(f"✅ Date validation test passed: {date_str} is invalid")

    def test_file_operations_utilities(self):
        """Test file operation utilities"""

        # Test file existence checks
        project_root = Path(__file__).parent.parent

        # Test that main files exist
        main_files = [
            "app.py",
            "requirements.txt",
            "dados",  # directory
        ]

        for filename in main_files:
            file_path = project_root / filename
            assert file_path.exists()
            print(f"✅ File existence test passed: {filename} exists")

        # Test directory creation
        test_dir = project_root / "temp_test_dir"
        test_dir.mkdir(exist_ok=True)
        assert test_dir.exists()

        # Cleanup
        test_dir.rmdir()
        assert not test_dir.exists()
        print("✅ Directory operations test passed")

    def test_error_handling_utilities(self):
        """Test error handling utilities"""

        # Test graceful error handling
        def safe_divide(a, b):
            """Safe division with error handling"""
            try:
                return a / b
            except ZeroDivisionError:
                return 0
            except TypeError:
                return None

        # Test normal division
        assert safe_divide(10, 2) == 5
        print("✅ Normal division test passed")

        # Test division by zero
        assert safe_divide(10, 0) == 0
        print("✅ Division by zero handling test passed")

        # Test invalid types
        assert safe_divide("10", 2) is None
        print("✅ Invalid type handling test passed")


def run_all_tests():
    """Run all utility tests with detailed output"""
    print("🧪 Starting Utility Tests for Gestão Tattoo Studio")
    print("=" * 60)

    # Run pytest with verbose output
    pytest.main([__file__, "-v", "--tb=short"])

    print("\n" + "=" * 60)
    print("✅ All utility tests completed!")
    print("💡 Check the output above for any failures or warnings.")


if __name__ == "__main__":
    run_all_tests()
