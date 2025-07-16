#!/usr/bin/env python3
"""
🧪 Test Data Generator for Gestão Tattoo Studio

This script generates realistic test data for the Tattoo Studio Management System.
All data uses May 2025 as the date range for consistency.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from random import choice, randint, uniform

# Add the parent directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test data for realistic generation
ARTISTS = [
    "Ana Silva",
    "Carlos Santos",
    "Maria Oliveira",
    "João Pereira",
    "Fernanda Costa",
]

CLIENTS = [
    "Pedro Almeida",
    "Julia Ferreira",
    "Roberto Lima",
    "Carolina Moura",
    "Lucas Barbosa",
    "Mariana Torres",
    "Diego Souza",
    "Amanda Ribeiro",
    "Gabriel Rocha",
    "Beatriz Campos",
]

PAYMENT_METHODS = ["Dinheiro", "Pix", "Crédito", "Débito"]

TATTOO_DESCRIPTIONS = [
    "Tatuagem pequena no pulso",
    "Mandala nas costas",
    "Frase no antebraço",
    "Flor no ombro",
    "Tribal na perna",
    "Retrato realista",
    "Geometric design",
    "Aquarela colorida",
    "Tradicional old school",
    "Minimalista geométrica",
]


def generate_test_sessions(num_sessions=15):
    """Generate realistic test sessions for May 2025"""
    sessions = []

    for i in range(num_sessions):
        # Random date in May 2025
        day = randint(1, 31)
        try:
            date = datetime(2025, 5, day).strftime("%Y-%m-%d")
        except ValueError:
            date = datetime(2025, 5, 28).strftime("%Y-%m-%d")

        # Random time
        hour = randint(9, 18)
        minute = choice([0, 15, 30, 45])
        time = f"{hour:02d}:{minute:02d}"

        # Random data
        client = choice(CLIENTS)
        artist = choice(ARTISTS)
        value = round(uniform(80, 500), 2)
        observations = choice(TATTOO_DESCRIPTIONS)

        base_date = datetime(2025, 5, day)
        fechamento_offset = randint(0, 5)
        fechamento_date = base_date + timedelta(days=fechamento_offset)
        session = {
            "id": i + 1,
            "cliente": client,
            "artista": artist,
            "data": date,
            "hora": time,
            "valor": value,
            "observacoes": observations,
            "data_fechamento": fechamento_date.strftime("%Y-%m-%d %H:%M:%S"),
            "paga": choice([True, False]),
            "comissao": round(value * 0.7, 2) if choice([True, False]) else 0.0,
        }

        sessions.append(session)

    return sessions


def generate_test_payments(num_payments=20):
    """Generate realistic test payments for May 2025"""
    payments = []

    for i in range(num_payments):
        # Random date in May 2025
        day = randint(1, 31)
        try:
            date = datetime(2025, 5, day).strftime("%Y-%m-%d")
        except ValueError:
            date = datetime(2025, 5, 28).strftime("%Y-%m-%d")

        client = choice(CLIENTS)
        artist = choice(ARTISTS)
        value = round(uniform(50, 800), 2)
        payment_method = choice(PAYMENT_METHODS)
        description = f"Pagamento - {choice(TATTOO_DESCRIPTIONS)}"

        payment = {
            "id": i + 1,
            "data": date,
            "cliente": client,
            "artista": artist,
            "valor": value,
            "forma_pagamento": payment_method,
            "descricao": description,
            "comissao": round(value * 0.7, 2) if choice([True, False]) else 0.0,
        }

        payments.append(payment)

    return payments


def generate_test_commissions(num_commissions=12):
    """Generate realistic test commissions for May 2025"""
    commissions = []

    for i in range(num_commissions):
        # Random date in May 2025
        day = randint(1, 31)
        try:
            date = datetime(2025, 5, day).strftime("%Y-%m-%d")
        except ValueError:
            date = datetime(2025, 5, 28).strftime("%Y-%m-%d")

        artist = choice(ARTISTS)
        client = choice(CLIENTS)
        total_value = round(uniform(100, 600), 2)
        commission_rate = uniform(0.6, 0.8)  # 60% to 80% commission
        commission_value = round(total_value * commission_rate, 2)

        commission = {
            "id": i + 1,
            "data": date,
            "artista": artist,
            "cliente": client,
            "valor_total": total_value,
            "valor_comissao": commission_value,
            "porcentagem": round(commission_rate * 100, 1),
            "descricao": f"Comissão - {choice(TATTOO_DESCRIPTIONS)}",
            "data_registro": datetime(2025, 5, day).strftime("%Y-%m-%d %H:%M:%S"),
        }

        commissions.append(commission)

    return commissions


def generate_test_artists():
    """Generate artist profiles with commission rates"""
    artists = []

    for i, artist_name in enumerate(ARTISTS):
        artist = {
            "id": i + 1,
            "nome": artist_name,
            "especialidade": choice(
                ["Realismo", "Tradicional", "Aquarela", "Tribal", "Minimalista"]
            ),
            "comissao_padrao": round(uniform(60, 80), 1),  # 60% to 80%
            "ativo": True,
            "data_cadastro": datetime(2025, 1, randint(1, 28)).strftime("%Y-%m-%d"),
        }
        artists.append(artist)

    return artists


def generate_test_expenses(num_expenses=10):
    """Generate realistic test expenses for May 2025"""
    expenses = []

    EXPENSE_CATEGORIES = ["Material", "Limpeza", "Manutenção", "Aluguel", "Outros"]
    EXPENSE_DESCRIPTIONS = [
        "Compra de tintas",
        "Agulhas descartáveis",
        "Produtos de limpeza",
        "Manutenção da máquina",
        "Aluguel do espaço",
        "Papel toalha",
        "Luvas descartáveis",
        "Desinfetante",
        "Material de proteção",
    ]

    for i in range(num_expenses):
        # Random date in May 2025
        day = randint(1, 31)
        try:
            date = datetime(2025, 5, day).strftime("%Y-%m-%d")
        except ValueError:
            date = datetime(2025, 5, 28).strftime("%Y-%m-%d")

        expense = {
            "id": i + 1,
            "data": date,
            "valor": round(uniform(20, 200), 2),
            "categoria": choice(EXPENSE_CATEGORIES),
            "descricao": choice(EXPENSE_DESCRIPTIONS),
            "forma_pagamento": choice(PAYMENT_METHODS),
        }

        expenses.append(expense)

    return expenses


def save_test_data_to_files():
    """Save all test data to JSON files"""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "dados"

    # Ensure data directory exists
    data_dir.mkdir(exist_ok=True)

    # Generate test data
    sessions = generate_test_sessions()
    payments = generate_test_payments()
    commissions = generate_test_commissions()
    artists = generate_test_artists()
    expenses = generate_test_expenses()

    # Prepare sessions data structure
    sessions_data = {
        "sessoes_ativas": sessions[:5],  # Some active sessions
        "historico": sessions[5:],  # Rest in history
        "limbo": sessions[2:4],  # Some in limbo
    }

    # Save to files
    files_to_save = {
        "sessoes.json": sessions_data,
        "pagamentos.json": payments,
        "comissoes.json": commissions,
        "despesas.json": expenses,
        "historico_sessoes.json": sessions[5:],
        "historico_pagamentos.json": payments[10:],
        "historico_comissoes.json": commissions[6:],
    }

    # Save artists to the cadastro_interno directory
    artists_dir = project_root / "cadastro_interno" / "dados"
    artists_dir.mkdir(exist_ok=True)

    with open(artists_dir / "artistas.json", "w", encoding="utf-8") as f:
        json.dump(artists, f, indent=4, ensure_ascii=False)

    print("🎨 Artists data saved to cadastro_interno/dados/artistas.json")

    # Save all other data files
    for filename, data in files_to_save.items():
        filepath = data_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(
            f"📄 {filename} saved with {len(data) if isinstance(data, list) else 'structured'} records"
        )


def print_data_summary():
    """Print a summary of the generated test data"""
    print("\n" + "=" * 50)
    print("📊 TEST DATA SUMMARY")
    print("=" * 50)
    print(f"📅 Date Range: May 2025")
    print(f"👥 Artists: {len(ARTISTS)}")
    print(f"👤 Clients: {len(CLIENTS)}")
    print(f"💳 Payment Methods: {len(PAYMENT_METHODS)}")
    print(f"🎨 Tattoo Descriptions: {len(TATTOO_DESCRIPTIONS)}")
    print("\nGenerated Data:")
    print(f"  • Sessions: ~15 (5 active, 10 in history, 2 in limbo)")
    print(f"  • Payments: ~20")
    print(f"  • Commissions: ~12")
    print(f"  • Expenses: ~10")
    print(f"  • Artists: {len(ARTISTS)}")
    print("=" * 50)


if __name__ == "__main__":
    print("🧪 Generating Test Data for Gestão Tattoo Studio...")
    print("📅 Using May 2025 as the date range for consistency")

    save_test_data_to_files()
    print_data_summary()

    print("\n✅ Test data generation completed!")
    print("💡 You can now run the Flask application to see the test data in action.")
    print("🔄 To regenerate test data, run this script again.")
