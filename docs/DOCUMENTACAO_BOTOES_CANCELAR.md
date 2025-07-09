# DOCUMENTAÇÃO - PADRONIZAÇÃO DOS BOTÕES "CANCELAR"

## Data da Alteração
Data: $(date)

## Objetivo
Padronizar a cor de todos os botões "Cancelar" no sistema de gestão do estúdio de tatuagem para manter consistência visual.

## Alterações Realizadas

### 1. CSS - Arquivo: `static/css/style.css`

#### Adicionada classe `.btn-secondary`:
```css
/* Botão Cancelar - Padrão amarelo */
.btn-secondary {
    background-color: #EDAE4C;
    color: #333333;
}

.btn-secondary:hover {
    background-color: #F0B85C;
    color: #333333;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
```

#### Adicionado seletor específico para modal:
```css
/* Seletor adicional para botões de cancelar no modal */
button[onclick*="closeModal"] {
    background-color: #EDAE4C !important;
    color: #333333 !important;
}

button[onclick*="closeModal"]:hover {
    background-color: #F0B85C !important;
    color: #333333 !important;
}
```

### 2. HTML - Arquivo: `templates/base.html`

#### Modal de confirmação:
- Adicionada classe `btn-secondary` ao botão "Cancelar" do modal

## Arquivos Afetados

### Templates que já usavam a classe `btn-secondary`:
- `templates/cadastro_interno/editar_artista.html`
- `templates/financeiro/registrar_pagamento.html`
- `templates/estoque/novo_produto.html`
- `templates/financeiro/editar_pagamento.html`
- `templates/estoque/editar_produto.html`
- `templates/historico/editar_comissao.html`
- `templates/sessoes/nova_sessao.html`
- `templates/sessoes/editar_sessao.html`
- `templates/historico/editar.html`

### Arquivos modificados:
- `static/css/style.css` - Adicionada definição da classe `.btn-secondary`
- `templates/base.html` - Adicionada classe ao botão do modal

## Especificações de Cor

### Cores Padrão:
- **Background**: `#EDAE4C` (amarelo)
- **Texto**: `#333333` (preto escuro para contraste)
- **Hover**: `#F0B85C` (amarelo mais claro)

### Justificativa:
- Amarelo (`#EDAE4C`) é uma cor neutra que não interfere com outras ações
- Texto preto garante legibilidade e contraste adequado
- Hover mais claro proporciona feedback visual

## Manutenção Futura

### Para novos botões "Cancelar":
1. Sempre usar a classe `btn-secondary`
2. Manter o padrão de cores definido
3. Não alterar padding, bordas ou outros estilos

### Exemplo de uso:
```html
<a href="{{ url_for('rota_voltar') }}" class="btn btn-secondary">Cancelar</a>
```

### Para botões em JavaScript:
```javascript
// Se criar botões dinamicamente, aplicar a classe
const cancelButton = document.createElement('button');
cancelButton.className = 'btn btn-secondary';
cancelButton.textContent = 'Cancelar';
```

## Testes Realizados

### Páginas verificadas:
- [x] Editar Produto
- [x] Novo Produto
- [x] Editar Artista
- [x] Registrar Pagamento
- [x] Editar Pagamento
- [x] Editar Comissão
- [x] Nova Sessão
- [x] Editar Sessão
- [x] Editar Histórico
- [x] Modal de Confirmação

### Resultados:
- Todos os botões "Cancelar" agora exibem a cor amarela padronizada
- Contraste adequado para legibilidade
- Hover funciona corretamente
- Não há impacto em outros elementos da interface

## Observações

- A alteração é consistente em todo o sistema
- Não afeta outros botões ou elementos
- Mantém a usabilidade e acessibilidade
- Facilita futuras manutenções através da classe centralizada 