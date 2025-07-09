# Sistema de Histórico Antigo - Tattoo Gestão

## Funcionalidades Implementadas

### 1. Correção dos Botões de Ação
- ✅ Botões "AÇÃO" agora aparecem sempre visíveis acima de qualquer elemento
- ✅ Posicionamento correto com `position: fixed` e `z-index: 999999`
- ✅ Cada botão funciona independentemente sem colisões
- ✅ JavaScript centralizado no template base

### 2. Correção de Texto
- ✅ "EXTRATO MENSUAL" corrigido para "EXTRATO MENSAL" no menu lateral

### 3. Funcionalidade de Histórico Antigo
- ✅ Duas opções de visualização:
  - **Histórico de Pagamentos**
  - **Histórico de Comissões por Artista**
- ✅ Seleção de mês para ambos os tipos
- ✅ Botão "BUSCAR EXTRATO" centralizado

### 4. Valor Líquido do Estúdio
- ✅ Exibição do valor total recebido no mês
- ✅ Soma das comissões dos artistas
- ✅ Cálculo e destaque do valor líquido do estúdio
- ✅ Layout visual destacado com gradientes

### 5. Movimentação Automática de Dados
- ✅ Script `mover_historico.py` para executar no primeiro dia de cada mês
- ✅ Movimentação automática de pagamentos e comissões para histórico antigo
- ✅ Criação de arquivos separados por mês e tipo

## Como Usar

### Executar Movimentação Automática
```bash
python mover_historico.py
```

### Acessar Históricos Antigos
1. Vá para o menu "HISTÓRICO"
2. Clique em "Históricos Antigos"
3. Selecione o tipo de histórico (Pagamentos ou Comissões)
4. Escolha o mês desejado
5. Clique em "BUSCAR EXTRATO"

### Estrutura de Arquivos
```
dados/
├── historico_antigo/
│   ├── pagamentos_2025-06.json
│   ├── comissoes_2025-06.json
│   ├── pagamentos_2025-05.json
│   └── comissoes_2025-05.json
├── pagamentos.json (dados do mês atual)
└── sessoes.json (dados do mês atual)
```

## Identidade Visual
- ✅ Tema escuro e minimalista
- ✅ Paleta oficial mantida:
  - Fundo: #333333
  - Blocos: #545454
  - Texto: #F2F2F2
  - Verde: #00C7B4
  - Vermelho: #FF445A
  - Amarelo: #EDAE4C
- ✅ Sem emojis, design limpo
- ✅ Responsivo para diferentes tamanhos de tela

## Rotas Backend
- `/extrato/dados/<mes_ano>` - Dados de pagamentos
- `/extrato/comissoes/<mes_ano>` - Dados de comissões
- `/historicos-antigos` - Página principal

## Observações Importantes
- A movimentação automática deve ser executada no primeiro dia de cada mês
- Os dados do mês anterior são automaticamente movidos para o histórico antigo
- O sistema mantém a integridade dos dados durante a movimentação
- Todos os botões de ação agora funcionam corretamente em todas as páginas 