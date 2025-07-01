from estoque.produtos import carregar_produtos, salvar_produtos

def registrar_entrada(produto_id, quantidade, preco_unitario):
    produtos = carregar_produtos()

    for produto in produtos:
        if produto["id"] == produto_id:
            estoque_antigo = produto["quantidade_estoque"]
            custo_antigo = produto["custo_medio"]

            # Novo custo médio ponderado
            total_antigo = estoque_antigo * custo_antigo
            total_novo = quantidade * preco_unitario
            nova_quantidade = estoque_antigo + quantidade

            novo_custo_medio = (total_antigo + total_novo) / nova_quantidade if nova_quantidade > 0 else preco_unitario

            produto["quantidade_estoque"] = nova_quantidade
            produto["custo_medio"] = round(novo_custo_medio, 2)

            salvar_produtos(produtos)
            print("Entrada registrada com sucesso.")
            return

    print("Produto não encontrado.")

def registrar_saida(produto_id, quantidade):
    produtos = carregar_produtos()

    for produto in produtos:
        if produto["id"] == produto_id:
            if produto["quantidade_estoque"] < quantidade:
                print("Erro: estoque insuficiente.")
                return

            produto["quantidade_estoque"] -= quantidade
            salvar_produtos(produtos)
            print("Saída registrada com sucesso.")

            if produto["quantidade_estoque"] < 5:  # Alerta de estoque baixo
                print(f"⚠ Estoque baixo: {produto['nome']} — {produto['quantidade_estoque']} unidades restantes.")
            return

    print("Produto não encontrado.")
