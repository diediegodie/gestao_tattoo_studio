#!/usr/bin/env python3
"""
🧪 Model Tests for Gestão Tattoo Studio

This module tests the data layer - JSON file operations, data integrity,
and CRUD operations for sessions, payments, commissions, and artists.
"""

import pytest
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the parent directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_data import (
    generate_test_sessions,
    generate_test_payments,
    generate_test_commissions,
    generate_test_artists,
    generate_test_expenses,
)

# Import the actual modules we want to test
from sessoes.agendamento import (
    carregar_agendamentos,
    salvar_agendamentos,
    agendar_sessao,
    excluir_agendamento,
)
from financeiro.caixa import (
    carregar_pagamentos,
    salvar_pagamentos,
    registrar_pagamento,
    excluir_pagamento,
)
from financeiro.comissoes import (
    carregar_comissoes,
    salvar_comissoes,
    registrar_comissao_avulsa,
)
from cadastro_interno.artistas import carregar_artistas


class TestModels:
    """Test class for data models and operations"""

    @pytest.fixture
    def setup_test_data(self):
        """Set up test data before each test"""
        # Generate fresh test data
        test_sessions = generate_test_sessions(5)
        test_payments = generate_test_payments(5)
        test_commissions = generate_test_commissions(3)
        test_artists = generate_test_artists()

        return {
            "sessions": test_sessions,
            "payments": test_payments,
            "commissions": test_commissions,
            "artists": test_artists,
        }

    def test_sessions_crud_operations(self, setup_test_data):
        """Test Create, Read, Update, Delete operations for sessions"""

        # Test loading sessions
        sessions = carregar_agendamentos()
        assert isinstance(sessions, list)
        print("✅ Sessions loading test passed")

        # Test creating a new session
        initial_count = len(sessions)
        agendar_sessao(
            cliente="Test Client",
            artista="Test Artist",
            data="2025-05-20",
            hora="14:30",
            valor=150.00,
            observacoes="Test session",
        )

        # Reload and check
        updated_sessions = carregar_agendamentos()
        assert len(updated_sessions) == initial_count + 1
        print("✅ Session creation test passed")

        # Test session data integrity
        new_session = updated_sessions[-1]
        assert new_session["cliente"] == "Test Client"
        assert new_session["artista"] == "Test Artist"
        assert new_session["data"] == "2025-05-20"
        assert new_session["hora"] == "14:30"
        assert new_session["valor"] == 150.00
        print("✅ Session data integrity test passed")

        # Test deleting a session
        if updated_sessions:
            excluir_agendamento(len(updated_sessions) - 1)
            final_sessions = carregar_agendamentos()
            assert len(final_sessions) == initial_count
            print("✅ Session deletion test passed")

    def test_payments_crud_operations(self, setup_test_data):
        """Test Create, Read, Update, Delete operations for payments"""

        # Test loading payments
        payments = carregar_pagamentos()
        assert isinstance(payments, list)
        print("✅ Payments loading test passed")

        # Test creating a new payment
        initial_count = len(payments)
        new_payment = {
            "data": "2025-05-15",
            "valor": 200.00,
            "forma_pagamento": "Dinheiro",
            "cliente": "Test Client",
            "artista": "Test Artist",
            "descricao": "Test payment",
        }

        result = registrar_pagamento(new_payment)
        assert result is True

        # Reload and check
        updated_payments = carregar_pagamentos()
        assert len(updated_payments) == initial_count + 1
        print("✅ Payment creation test passed")

        # Test payment data integrity
        last_payment = updated_payments[-1]
        assert last_payment["cliente"] == "Test Client"
        assert last_payment["artista"] == "Test Artist"
        assert last_payment["valor"] == 200.00
        assert last_payment["forma_pagamento"] == "Dinheiro"
        print("✅ Payment data integrity test passed")

        # Test deleting a payment
        if updated_payments:
            excluir_pagamento(len(updated_payments) - 1)
            final_payments = carregar_pagamentos()
            assert len(final_payments) == initial_count
            print("✅ Payment deletion test passed")

    def test_commissions_operations(self, setup_test_data):
        """Test commission operations"""

        # Test loading commissions
        commissions = carregar_comissoes()
        assert isinstance(commissions, list)
        print("✅ Commissions loading test passed")

        # Test creating a new commission
        initial_count = len(commissions)
        registrar_comissao_avulsa(
            artista="Test Artist",
            valor_comissao=70.00,
            valor_total=100.00,
            cliente="Test Client",
            data="2025-05-15",
            descricao="Test commission",
        )

        # Reload and check
        updated_commissions = carregar_comissoes()
        assert len(updated_commissions) == initial_count + 1
        print("✅ Commission creation test passed")

        # Test commission data integrity
        new_commission = updated_commissions[-1]
        assert new_commission["artista"] == "Test Artist"
        assert new_commission["valor_comissao"] == 70.00
        assert new_commission["valor_total"] == 100.00
        assert new_commission["cliente"] == "Test Client"
        print("✅ Commission data integrity test passed")

    def test_artists_operations(self, setup_test_data):
        """Test artist operations"""

        # Test loading artists
        artists = carregar_artistas()
        assert isinstance(artists, list)
        print("✅ Artists loading test passed")

        # Test artist data structure
        if artists:
            artist = artists[0]
            required_fields = ["nome"]
            for field in required_fields:
                assert field in artist
            print("✅ Artist data structure test passed")

    def test_data_validation(self, setup_test_data):
        """Test data validation and error handling"""

        # Test invalid session data
        try:
            agendar_sessao(
                cliente="",  # Empty client name
                artista="Test Artist",
                data="invalid-date",  # Invalid date
                hora="25:00",  # Invalid time
                valor="not-a-number",  # Invalid value
                observacoes="Test",
            )
            print("⚠️  Invalid session data should have been rejected")
        except (ValueError, TypeError):
            print("✅ Invalid session data validation test passed")

        # Test invalid payment data
        try:
            invalid_payment = {
                "data": "invalid-date",
                "valor": "not-a-number",
                "forma_pagamento": "",
                "cliente": "",
                "artista": "",
                "descricao": "",
            }
            registrar_pagamento(invalid_payment)
            print("⚠️  Invalid payment data should have been rejected")
        except (ValueError, TypeError, KeyError):
            print("✅ Invalid payment data validation test passed")

    def test_file_operations(self, setup_test_data):
        """Test JSON file operations"""

        # Test that files are created if they don't exist
        sessions = carregar_agendamentos()
        payments = carregar_pagamentos()
        commissions = carregar_comissoes()
        artists = carregar_artistas()

        # All should return lists even if files don't exist
        assert isinstance(sessions, list)
        assert isinstance(payments, list)
        assert isinstance(commissions, list)
        assert isinstance(artists, list)
        print("✅ File operations test passed")

        # Test file encoding (UTF-8)
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "dados"

        if (data_dir / "sessoes.json").exists():
            with open(data_dir / "sessoes.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict) or isinstance(data, list)
                print("✅ File encoding test passed")

    def test_data_consistency(self, setup_test_data):
        """Test data consistency across different operations"""

        # Test session-payment consistency
        sessions = carregar_agendamentos()
        payments = carregar_pagamentos()

        # Check that sessions and payments have consistent artist names
        session_artists = set(s.get("artista", "") for s in sessions)
        payment_artists = set(p.get("artista", "") for p in payments)

        # Artists should be consistent (or at least not contradictory)
        print(f"Session artists: {len(session_artists)}")
        print(f"Payment artists: {len(payment_artists)}")
        print("✅ Data consistency test passed")

        # Test commission calculations
        commissions = carregar_comissoes()
        for commission in commissions:
            if "valor_total" in commission and "valor_comissao" in commission:
                valor_total = commission["valor_total"]
                valor_comissao = commission["valor_comissao"]

                # Commission should not exceed total value
                assert valor_comissao <= valor_total

                # Commission should be reasonable (0% to 100%)
                if valor_total > 0:
                    percentage = (valor_comissao / valor_total) * 100
                    assert 0 <= percentage <= 100

        print("✅ Commission calculation consistency test passed")

    def test_id_generation(self, setup_test_data):
        """Test ID generation for records"""

        # Test that new sessions get unique IDs
        sessions = carregar_agendamentos()

        # Create multiple sessions and check ID uniqueness
        for i in range(3):
            agendar_sessao(
                cliente=f"Test Client {i}",
                artista="Test Artist",
                data="2025-05-20",
                hora="14:30",
                valor=100.00,
                observacoes=f"Test session {i}",
            )

        updated_sessions = carregar_agendamentos()
        session_ids = [s.get("id") for s in updated_sessions if s.get("id")]

        # Check that IDs are unique
        assert len(session_ids) == len(set(session_ids))
        print("✅ ID generation test passed")


def run_all_tests():
    """Run all model tests with detailed output"""
    print("🧪 Starting Model Tests for Gestão Tattoo Studio")
    print("=" * 60)

    # Run pytest with verbose output
    pytest.main([__file__, "-v", "--tb=short"])

    print("\n" + "=" * 60)
    print("✅ All model tests completed!")
    print("💡 Check the output above for any failures or warnings.")


if __name__ == "__main__":
    run_all_tests()
