import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CAMINHO_ARQUIVO = BASE_DIR / "dados" / "sessoes.json"


def gerar_novo_id_historico(historico):
    """Gera um novo ID único para o histórico."""
    if not historico:
        return 1
    return max(int(s.get("id", 0)) for s in historico) + 1

def mover_para_historico(sessao_id: int, valor_final: float, comissao: float = 0.0):
    """
    Move uma sessão da lista de ativas para o histórico e a remove da lista de ativas,
    garantindo que o ID no histórico seja único.
    Também grava a sessão em historico_sessoes.json.
    """
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return False  # Não há o que mover se o arquivo não existe

    sessoes_ativas = dados.get("sessoes_ativas", [])
    historico = dados.get("historico", [])
    
    sessao_para_mover = None
    indice_sessao = -1

    # Encontra a sessão e seu índice na lista de ativas
    for i, sessao in enumerate(sessoes_ativas):
        if int(sessao.get("id", -1)) == int(sessao_id):
            sessao_para_mover = sessao
            indice_sessao = i
            break

    if not sessao_para_mover:
        return False  # Sessão não encontrada

    # Remove a sessão da lista de ativas
    sessoes_ativas.pop(indice_sessao)

    # Gera novo ID único para o histórico
    novo_id = gerar_novo_id_historico(historico)

    # Cria o novo registro para o histórico com o valor correto e ID único
    sessao_historico = {
        "id": novo_id,
        "cliente": sessao_para_mover["cliente"],
        "artista": sessao_para_mover["artista"],
        "data": sessao_para_mover["data"],
        "hora": sessao_para_mover["hora"],
        "valor": valor_final,
        "observacoes": sessao_para_mover.get("observacoes", ""),
        "data_fechamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paga": True,
        "comissao": comissao
    }
    historico.append(sessao_historico)

    # Salva também no arquivo historico_sessoes.json
    try:
        from pathlib import Path
        caminho_hist = Path(__file__).parent.parent / "dados" / "historico_sessoes.json"
        try:
            with open(caminho_hist, "r", encoding="utf-8") as f:
                historico_sessoes = json.load(f)
        except Exception:
            historico_sessoes = []
        # Evita duplicidade: só adiciona se não existir sessão igual
        if not any(str(s.get('id')) == str(sessao_historico['id']) and s.get('cliente') == sessao_historico['cliente'] for s in historico_sessoes):
            historico_sessoes.append(sessao_historico)
        with open(caminho_hist, "w", encoding="utf-8") as f:
            json.dump(historico_sessoes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar no historico_sessoes.json: {e}")

    # Prepara os dados para salvar de volta no arquivo original
    dados_atualizados = {
        "sessoes_ativas": sessoes_ativas,
        "historico": historico
    }
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados_atualizados, arquivo, indent=4, ensure_ascii=False)
    return True
