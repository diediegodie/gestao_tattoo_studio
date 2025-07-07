import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CAMINHO_COMISSOES = BASE_DIR / "dados" / "comissoes.json"


def carregar_comissoes():
    """Carrega as comissões avulsas do arquivo JSON."""
    try:
        with open(CAMINHO_COMISSOES, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_comissoes(comissoes):
    """Salva as comissões avulsas no arquivo JSON."""
    try:
        # Garante que o diretório existe
        CAMINHO_COMISSOES.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CAMINHO_COMISSOES, "w", encoding="utf-8") as arquivo:
            json.dump(comissoes, arquivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar comissões: {e}")
        return False


def gerar_id_comissao(comissoes):
    """Gera um novo ID único para comissão."""
    if not comissoes:
        return 1
    return max(int(c.get("id", 0)) for c in comissoes) + 1


def registrar_comissao_avulsa(artista, valor_comissao, valor_total, cliente, data, descricao=""):
    """
    Registra uma comissão avulsa (sem vínculo com sessão) no histórico.
    
    Args:
        artista (str): Nome do artista
        valor_comissao (float): Valor da comissão
        valor_total (float): Valor total do pagamento
        cliente (str): Nome do cliente
        data (str): Data do pagamento
        descricao (str): Descrição adicional (opcional)
    
    Returns:
        bool: True se registrado com sucesso, False caso contrário
    """
    try:
        comissoes = carregar_comissoes()
        
        nova_comissao = {
            "id": gerar_id_comissao(comissoes),
            "artista": artista,
            "valor_comissao": valor_comissao,
            "valor_total": valor_total,
            "cliente": cliente,
            "data": data,
            "data_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "descricao": descricao,
            "tipo": "pagamento_avulso"
        }
        
        comissoes.append(nova_comissao)
        
        if salvar_comissoes(comissoes):
            print(f"Comissão avulsa registrada: {artista} - R$ {valor_comissao:.2f}")
            return True
        else:
            print("Erro ao salvar comissão avulsa")
            return False
            
    except Exception as e:
        print(f"Erro ao registrar comissão avulsa: {e}")
        return False


def obter_comissoes_por_artista(artista=None, mes=None, ano=None):
    """
    Obtém comissões por artista, opcionalmente filtradas por mês e ano.
    
    Args:
        artista (str): Nome do artista (opcional)
        mes (int): Mês para filtrar (opcional)
        ano (int): Ano para filtrar (opcional)
    
    Returns:
        list: Lista de comissões filtradas
    """
    comissoes = carregar_comissoes()
    
    if artista:
        comissoes = [c for c in comissoes if c.get("artista") == artista]
    
    if mes and ano:
        comissoes_filtradas = []
        for comissao in comissoes:
            try:
                data_comissao = datetime.strptime(comissao["data"], "%Y-%m-%d")
                if data_comissao.month == mes and data_comissao.year == ano:
                    comissoes_filtradas.append(comissao)
            except ValueError:
                continue
        comissoes = comissoes_filtradas
    
    return comissoes


def calcular_total_comissoes_artista(artista, mes=None, ano=None):
    """
    Calcula o total de comissões de um artista em um período específico.
    
    Args:
        artista (str): Nome do artista
        mes (int): Mês para filtrar (opcional)
        ano (int): Ano para filtrar (opcional)
    
    Returns:
        float: Total de comissões do artista
    """
    comissoes = obter_comissoes_por_artista(artista, mes, ano)
    return sum(c.get("valor_comissao", 0) for c in comissoes) 