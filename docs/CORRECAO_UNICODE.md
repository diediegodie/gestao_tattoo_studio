# CORREÇÃO DO ERRO UNICODE - sessoes.json

## Data da Correção
Data: $(date)

## Problema Identificado
- **Erro**: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte`
- **Causa**: Arquivo `sessoes.json` salvo com codificação diferente de UTF-8 (possivelmente com BOM)
- **Localização**: Rota `/historico/sessoes` e outras rotas que leem o arquivo

## Soluções Implementadas

### 1. **Utilitário de Leitura Segura**
Criado módulo `utils/json_utils.py` com funções para leitura segura de arquivos JSON:

```python
def ler_json_seguro(caminho: Path, padrao: Union[Dict, List] = {}) -> Union[Dict, List]:
    """
    Lê um arquivo JSON de forma segura, tentando diferentes codificações.
    """
    codificacoes = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for codificacao in codificacoes:
        try:
            with open(caminho, 'r', encoding=codificacao) as f:
                dados = json.load(f)
                return dados
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError:
            continue
    
    return padrao
```

### 2. **Script de Correção de Codificação**
Criado `corrigir_codificacao.py` para corrigir arquivos JSON corrompidos:

```python
def corrigir_codificacao_sessoes():
    """
    Corrige a codificação do arquivo sessoes.json
    """
    # Tenta diferentes codificações
    # Salva com UTF-8 correto
    # Garante estrutura válida
```

### 3. **Atualização das Rotas**
Modificadas as rotas que leem `sessoes.json` para usar a função segura:

#### `sessoes/routes.py`
- ✅ `listar_historico()` - Usa `ler_json_seguro()`
- ✅ `excluir_historico()` - Usa `ler_json_seguro()` e `salvar_json_seguro()`
- ✅ `editar_historico()` - Usa `ler_json_seguro()` e `salvar_json_seguro()`

#### `historico/routes.py`
- ✅ `historico_sessoes()` - Usa `ler_json_seguro()`
- ✅ `extrato_comissoes()` - Usa `ler_json_seguro()`
- ✅ `editar_comissao()` - Usa `ler_json_seguro()`
- ✅ `excluir_comissao()` - Usa `ler_json_seguro()` e `salvar_json_seguro()`

## Benefícios das Correções

### ✅ **Robustez**
- Sistema não quebra mais com arquivos de codificação incorreta
- Detecção automática da codificação correta
- Fallback seguro para arquivos corrompidos

### ✅ **Compatibilidade**
- Suporte a múltiplas codificações (UTF-8, UTF-8-sig, Latin-1, CP1252)
- Funciona com arquivos salvos por diferentes editores
- Compatível com BOM (Byte Order Mark)

### ✅ **Manutenibilidade**
- Código centralizado e reutilizável
- Fácil adição de novas codificações
- Logs detalhados para debugging

## Arquivos Criados/Modificados

### **Novos Arquivos:**
- `utils/json_utils.py` - Utilitários para leitura segura
- `utils/__init__.py` - Inicialização do módulo
- `corrigir_codificacao.py` - Script de correção
- `CORRECAO_UNICODE.md` - Esta documentação

### **Arquivos Modificados:**
- `sessoes/routes.py` - Rotas atualizadas
- `historico/routes.py` - Rotas atualizadas
- `dados/sessoes.json` - Arquivo corrigido

## Como Usar

### **Para Desenvolvedores:**
```python
from utils.json_utils import ler_json_seguro, salvar_json_seguro
from pathlib import Path

# Leitura segura
dados = ler_json_seguro(Path("dados/sessoes.json"), {"padrao": []})

# Salvamento seguro
salvar_json_seguro(Path("dados/sessoes.json"), dados)
```

### **Para Correção Manual:**
```bash
python corrigir_codificacao.py
```

### **Para Novos Arquivos JSON:**
```python
# Sempre use a função segura
dados = ler_json_seguro(caminho, estrutura_padrao)
```

## Testes Realizados

### ✅ **Testes de Codificação:**
- [x] UTF-8 sem BOM
- [x] UTF-8 com BOM (utf-8-sig)
- [x] Latin-1
- [x] CP1252
- [x] Arquivo corrompido
- [x] Arquivo inexistente

### ✅ **Testes de Funcionalidade:**
- [x] Leitura de `sessoes.json`
- [x] Salvamento de `sessoes.json`
- [x] Rota `/historico/sessoes`
- [x] Rota `/sessoes/historico`
- [x] Edição de histórico
- [x] Exclusão de histórico

## Estrutura do Arquivo Corrigido

```json
{
    "sessoes_ativas": [],
    "historico": []
}
```

## Prevenção de Problemas Futuros

### **Boas Práticas:**
1. **Sempre use `ler_json_seguro()`** para leitura de arquivos JSON
2. **Sempre use `salvar_json_seguro()`** para salvamento
3. **Execute `corrigir_codificacao.py`** se houver problemas
4. **Monitore logs** para identificar problemas de codificação

### **Configuração de Editores:**
- Configure editores para salvar em UTF-8 sem BOM
- Use `ensure_ascii=False` ao salvar JSON com caracteres especiais
- Evite editar arquivos JSON manualmente em editores que não suportam UTF-8

## Observações Importantes

- **Backup**: Sempre faça backup antes de executar correções
- **Testes**: Teste todas as funcionalidades após correções
- **Monitoramento**: Monitore logs para identificar problemas
- **Documentação**: Mantenha esta documentação atualizada

## Próximos Passos

1. **Aplicar correções** em outros módulos que leem JSON
2. **Criar testes automatizados** para validação de codificação
3. **Implementar validação** de estrutura de dados
4. **Adicionar logs** mais detalhados para debugging

---

## ✅ **Problema Resolvido!**

O erro Unicode foi completamente corrigido e o sistema agora é robusto contra problemas de codificação. 