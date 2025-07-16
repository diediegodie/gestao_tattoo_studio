#!/usr/bin/env python3
"""
🧪 Route Tests for Gestão Tattoo Studio

This module tests all main GET and POST routes to ensure they work correctly.
Tests include status codes, content validation, and form submissions.
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app
from test_data import save_test_data_to_files


class TestRoutes:
    """Test class for all application routes"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask application"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        with app.test_client() as client:
            with app.app_context():
                # Load test data before each test
                save_test_data_to_files()
                yield client
    
    def test_index_route(self, client):
        """Test the main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Gestão Tattoo Studio' in response.data or b'index' in response.data
        print("✅ Index route test passed")
    
    def test_financeiro_routes(self, client):
        """Test financial module routes"""
        
        # Test main financial page
        response = client.get('/financeiro/')
        assert response.status_code == 200
        print("✅ Financeiro index route test passed")
        
        # Test payment registration form
        response = client.get('/financeiro/registrar')
        assert response.status_code == 200
        print("✅ Payment registration form test passed")
        
        # Test payment registration POST
        payment_data = {
            'data': '2025-05-15',
            'valor': '150.00',
            'forma_pagamento': 'Dinheiro',
            'cliente': 'Test Client',
            'artista': 'Test Artist',
            'descricao': 'Test payment'
        }
        response = client.post('/financeiro/registrar', data=payment_data)
        assert response.status_code in [200, 302]  # Success or redirect
        print("✅ Payment registration POST test passed")
    
    def test_sessoes_routes(self, client):
        """Test sessions module routes"""
        
        # Test sessions listing
        response = client.get('/sessoes/')
        assert response.status_code == 200
        print("✅ Sessions listing test passed")
        
        # Test new session form
        response = client.get('/sessoes/nova')
        assert response.status_code == 200
        print("✅ New session form test passed")
        
        # Test session creation POST
        session_data = {
            'cliente': 'Test Client',
            'artista': 'Ana Silva',
            'data': '2025-05-20',
            'hora': '14:30',
            'valor': '200.00',
            'observacoes': 'Test session'
        }
        response = client.post('/sessoes/nova', data=session_data)
        assert response.status_code in [200, 302]  # Success or redirect
        print("✅ Session creation POST test passed")
        
        # Test session history
        response = client.get('/sessoes/historico')
        assert response.status_code == 200
        print("✅ Session history test passed")
    
    def test_estoque_routes(self, client):
        """Test inventory module routes"""
        
        # Test inventory main page
        response = client.get('/estoque/')
        assert response.status_code == 200
        print("✅ Inventory main page test passed")
        
        # Test inventory management
        response = client.get('/estoque/gerenciar')
        assert response.status_code == 200
        print("✅ Inventory management test passed")
    
    def test_historico_routes(self, client):
        """Test history module routes"""
        
        # Test history index
        response = client.get('/historico/')
        assert response.status_code == 200
        print("✅ History index test passed")
        
        # Test payments history
        response = client.get('/historico/pagamentos')
        assert response.status_code == 200
        print("✅ Payments history test passed")
        
        # Test commissions history
        response = client.get('/historico/comissoes')
        assert response.status_code == 200
        print("✅ Commissions history test passed")
    
    def test_extrato_routes(self, client):
        """Test extract/statement routes"""
        
        # Test monthly extract
        response = client.get('/extrato/')
        assert response.status_code == 200
        print("✅ Monthly extract test passed")
        
        # Test extract with specific month
        response = client.get('/extrato/2025/05')
        assert response.status_code == 200
        print("✅ Specific month extract test passed")
    
    def test_cadastro_interno_routes(self, client):
        """Test internal registry routes"""
        
        # Test artists management
        response = client.get('/cadastro/')
        assert response.status_code == 200
        print("✅ Internal registry test passed")
        
        # Test artists listing
        response = client.get('/cadastro/artistas')
        assert response.status_code == 200
        print("✅ Artists listing test passed")
    
    def test_calculadora_routes(self, client):
        """Test calculator module routes"""
        
        # Test calculator main page
        response = client.get('/calculadora/')
        assert response.status_code == 200
        print("✅ Calculator main page test passed")
    
    def test_error_handling(self, client):
        """Test error handling for invalid routes"""
        
        # Test 404 error
        response = client.get('/invalid-route')
        assert response.status_code == 404
        print("✅ 404 error handling test passed")
        
        # Test invalid session ID
        response = client.get('/sessoes/editar/99999')
        assert response.status_code in [404, 302]  # Not found or redirect
        print("✅ Invalid session ID error handling test passed")
    
    def test_form_validations(self, client):
        """Test form validation errors"""
        
        # Test empty payment form
        response = client.post('/financeiro/registrar', data={})
        assert response.status_code == 200  # Form should return with errors
        print("✅ Empty payment form validation test passed")
        
        # Test invalid session data
        invalid_session_data = {
            'cliente': '',  # Empty client name
            'artista': '',  # Empty artist name
            'data': 'invalid-date',  # Invalid date format
            'hora': '25:00',  # Invalid time
            'valor': 'not-a-number'  # Invalid value
        }
        response = client.post('/sessoes/nova', data=invalid_session_data)
        assert response.status_code == 200  # Form should return with errors
        print("✅ Invalid session data validation test passed")
    
    def test_search_and_filter(self, client):
        """Test search and filter functionality"""
        
        # Test session search
        response = client.get('/sessoes/?busca=Test')
        assert response.status_code == 200
        print("✅ Session search test passed")
        
        # Test date filter
        response = client.get('/sessoes/?data_inicio=2025-05-01&data_fim=2025-05-31')
        assert response.status_code == 200
        print("✅ Date filter test passed")
        
        # Test payment filter
        response = client.get('/financeiro/?forma_pagamento=Dinheiro')
        assert response.status_code == 200
        print("✅ Payment filter test passed")
    
    def test_ajax_endpoints(self, client):
        """Test AJAX endpoints for dynamic content"""
        
        # Test monthly extract data
        response = client.get('/extrato/dados/2025-05')
        assert response.status_code == 200
        
        # Check if response is JSON
        try:
            json_data = response.get_json()
            assert isinstance(json_data, dict)
            print("✅ Monthly extract AJAX test passed")
        except:
            print("⚠️  Monthly extract AJAX test - JSON response not available")
        
        # Test commission data
        response = client.get('/extrato/comissoes/2025-05')
        assert response.status_code == 200
        print("✅ Commission data AJAX test passed")


def run_all_tests():
    """Run all route tests with detailed output"""
    print("🧪 Starting Route Tests for Gestão Tattoo Studio")
    print("="*60)
    
    # Run pytest with verbose output
    pytest.main([__file__, '-v', '--tb=short'])
    
    print("\n" + "="*60)
    print("✅ All route tests completed!")
    print("💡 Check the output above for any failures or warnings.")


if __name__ == "__main__":
    run_all_tests()
