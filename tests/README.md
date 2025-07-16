# 🧪 Tests for Gestão Tattoo Studio

This folder contains comprehensive tests for the Tattoo Studio Management System.

## 📋 Test Files

- **`test_data.py`** - Generates fake but realistic test data
- **`test_routes.py`** - Tests all main GET and POST routes
- **`test_models.py`** - Tests data layer operations
- **`test_utils.py`** - Tests utility functions
- **`test_manual_checklist.md`** - Manual testing checklist

## 🚀 How to Run Tests

### Prerequisites
```bash
pip install pytest pytest-flask
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_routes.py

# Run with verbose output
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=.
```

### Loading Test Data
```python
# To load test data for manual testing
python tests/test_data.py
```

## 📊 Test Data Overview

The test data includes:
- **Sessions**: Various sessions with different artists and clients
- **Payments**: Payment records with different methods
- **Commissions**: Commission calculations for artists
- **Artists**: Artist profiles with different commission rates
- **Clients**: Client information for sessions

All test data uses **May 2025** as the date range for consistency and easy filtering.

## 🔧 Test Configuration

Tests use isolated test data that doesn't interfere with production data. Each test file includes setup and teardown procedures to ensure clean test environments.

## 📝 Notes

- Tests cover both happy path and error scenarios
- Data validation is tested thoroughly
- API endpoints are tested for correct status codes and content
- Edge cases are included for robust testing
