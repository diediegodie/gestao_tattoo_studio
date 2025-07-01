from sessoes.procedimentos import carregar_agendamentos
from collections import defaultdict
from datetime import datetime


def gerar_extrato_comissoes(mes=None, ano=None):
    agendamentos = carregar_agendamentos()
    comissoes_por_artista = defaultdict(float)
    hoje = datetime.now()

    mes = mes or hoje.month
    ano = ano or hoje.year

    for sessao in agendamentos:
        if not sessao.get("paga"):
            continue

        data_sessao = datetime.strptime(sessao["data"], "%Y-%m-%d")
        if data_sessao.month != mes or data_sessao.year != ano:
            continue

        artista = sessao["artista"]
        comissao = sessao.get("comissao_artista", 0.0)
        comissoes_por_artista[artista] += comissao

    print(f"\n💰 EXTRATO DE COMISSÕES — {mes:02}/{ano}")
    for artista, total in comissoes_por_artista.items():
        print(f" - {artista}: R$ {total:.2f}")
