from sessoes.procedimentos import carregar_agendamentos, salvar_agendamentos
from financeiro.caixa import carregar_pagamentos, salvar_pagamentos
from datetime import datetime


def fechar_sessao(id_agendamento, valor_pago, forma_pagamento, porcentagem_comissao):
    agendamentos = carregar_agendamentos()
    pagamentos = carregar_pagamentos()
    hoje = datetime.now().strftime("%Y-%m-%d")

    sessao = next((s for s in agendamentos if s["id"] == id_agendamento), None)
    if not sessao:
        print("Sessão não encontrada.")
        return

    if sessao.get("paga"):
        print("Sessão já está fechada.")
        return

    # Calcula comissão
    comissao = round(valor_pago * (porcentagem_comissao / 100), 2)
    artista = sessao["artista"]
    cliente = sessao["cliente"]
    descricao = f"Sessão com {cliente} — Artista: {artista}"

    # Adiciona no caixa
    novo_pagamento = {
        "data": hoje,
        "valor": float(valor_pago),
        "forma_pagamento": forma_pagamento.lower(),
        "cliente": cliente,
        "descricao": descricao,
    }
    pagamentos.append(novo_pagamento)
    salvar_pagamentos(pagamentos)

    # Marca sessão como paga e salva com comissão
    sessao["valor_pago"] = valor_pago
    sessao["forma_pagamento"] = forma_pagamento.lower()
    sessao["comissao_artista"] = comissao
    sessao["paga"] = True

    salvar_agendamentos(agendamentos)

    print(f"Sessão fechada com sucesso. Comissão: R$ {comissao:.2f}")
