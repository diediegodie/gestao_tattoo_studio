# 🎨 Sistema de Gestão de Tattoo Studio

Sistema completo para gestão de estúdio de tatuagem, incluindo agendamento, financeiro, estoque e histórico.

## 🚀 **Início Rápido**

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Inicializar Dados**
```bash
python utils/inicializar_dados.py
```

### **3. Executar Sistema**
```bash
python run.py
```

### **4. Acessar Sistema**
- **URL**: http://localhost:5000
- **Módulos**: Sessões, Financeiro, Estoque, Histórico, Calculadora

## 📁 **Estrutura do Projeto**

```
gestao_tattoo_studio/
├── 📁 docs/                    # Documentação e correções
├── 📁 utils/                   # Scripts utilitários
├── 📁 dados/                   # Arquivos JSON de dados
├── 📁 sessoes/                 # Módulo de sessões
├── 📁 financeiro/              # Módulo financeiro
├── 📁 estoque/                 # Módulo de estoque
├── 📁 historico/               # Módulo de histórico
├── 📁 cadastro_interno/        # Cadastro de artistas
├── 📁 calculadora/             # Calculadora de preços
├── 📁 seguranca/               # Módulo de segurança
├── 📁 templates/               # Templates HTML
├── 📁 static/                  # Arquivos estáticos (CSS, JS)
├── app.py                      # Aplicação principal Flask
├── run.py                      # Script de execução
└── requirements.txt            # Dependências Python
```

## 🔧 **Módulos Principais**

### **📅 Sessões**
- Agendamento de sessões
- Controle de histórico
- Gestão de clientes e artistas

### **💰 Financeiro**
- Controle de caixa
- Comissões de artistas
- Extrato mensal
- Despesas

### **📦 Estoque**
- Controle de produtos
- Inventário
- Alertas de estoque baixo

### **📊 Histórico**
- Relatórios de sessões
- Extratos de comissões
- Dados históricos

## 🛠️ **Utilitários**

### **Scripts Disponíveis:**
- `utils/corrigir_codificacao.py` - Corrige problemas de codificação
- `utils/inicializar_dados.py` - Inicializa arquivos JSON
- `utils/mover_historico.py` - Move dados para histórico

### **Funções Utilitárias:**
```python
from utils.json_utils import ler_json_seguro, salvar_json_seguro
```

## 📚 **Documentação**

Toda a documentação está organizada na pasta `docs/`:

- **[docs/README.md](docs/README.md)** - Documentação completa
- **[docs/INSTRUCOES_ACESSO.md](docs/INSTRUCOES_ACESSO.md)** - Como usar o sistema
- **[docs/CORRECOES_ERRO_500.md](docs/CORRECOES_ERRO_500.md)** - Correções de erros
- **[docs/CORRECAO_UNICODE.md](docs/CORRECAO_UNICODE.md)** - Correção Unicode

## ✅ **Status do Sistema**

- 🟢 **Sistema 100% Funcional**
- 🟢 **Todas as rotas acessíveis**
- 🟢 **Arquivos JSON válidos**
- 🟢 **Interface padronizada**

## 🔍 **Solução de Problemas**

### **Erro 500:**
```bash
python utils/inicializar_dados.py
```

### **Problemas de Codificação:**
```bash
python utils/corrigir_codificacao.py
```

### **Problemas de Acesso:**
Consulte [docs/INSTRUCOES_ACESSO.md](docs/INSTRUCOES_ACESSO.md)

## 📞 **Suporte**

Para problemas ou dúvidas, consulte a documentação em `docs/` ou verifique os logs do sistema.

---

**Versão**: 1.0.0  
**Última atualização**: $(date)


