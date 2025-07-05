# Sistema de Gestão para Estúdio de Tatuagem

Sistema completo para gerenciamento de estúdio de tatuagem, incluindo agendamentos, estoque, financeiro e histórico.

## 🚀 Funcionalidades

- **📅 Agendamento de Sessões**: Cadastro e gerenciamento de sessões de tatuagem
- **📦 Controle de Estoque**: Gestão de produtos e materiais
- **💰 Financeiro**: Registro de pagamentos e controle financeiro
- **👥 Cadastro de Artistas**: Gerenciamento da equipe
- **🧮 Calculadora**: Cálculo de comissões e valores
- **📋 Histórico**: Acompanhamento de sessões finalizadas
- **📊 Relatórios**: Extratos mensais e relatórios financeiros

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd tattoo_gestao
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

6. **Execute o sistema**
```bash
python run.py
```

O sistema estará disponível em: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
tattoo_gestao/
├── app.py                 # Aplicação principal Flask
├── run.py                 # Script de execução
├── requirements.txt       # Dependências Python
├── env.example           # Exemplo de configuração
├── README.md             # Este arquivo
├── dados/                # Arquivos de dados JSON
├── static/               # Arquivos estáticos (CSS, JS)
├── templates/            # Templates HTML
├── sessoes/             # Módulo de agendamentos
├── estoque/             # Módulo de controle de estoque
├── financeiro/          # Módulo financeiro
├── cadastro_interno/    # Módulo de cadastro de artistas
├── calculadora/         # Módulo de cálculos
└── historico/           # Módulo de histórico
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
# Chave secreta para sessões
SECRET_KEY=sua_chave_secreta_aqui

# Modo de debug
DEBUG=True

# Configurações do servidor
HOST=0.0.0.0
PORT=5000
```

## 📖 Como Usar

### 1. Primeiro Acesso
- Acesse o sistema em `http://localhost:5000`
- Comece cadastrando os artistas no menu "Cadastro Interno"

### 2. Agendamento de Sessões
- Vá para "Sessões" no menu
- Clique em "Agendar nova sessão"
- Preencha os dados do cliente, artista, data e valor

### 3. Controle de Estoque
- Acesse "Estoque" no menu
- Cadastre produtos com nome, descrição e quantidade
- Monitore o estoque disponível

### 4. Financeiro
- Registre pagamentos em "Financeiro"
- Consulte extratos mensais
- Acompanhe receitas e despesas

### 5. Histórico
- Visualize sessões finalizadas
- Acompanhe o histórico de pagamentos

## 🔒 Segurança

- O sistema usa arquivos JSON para armazenamento local
- Recomenda-se implementar autenticação para produção
- Faça backup regular dos arquivos em `dados/`

## 🚀 Deploy em Produção

Para usar em produção:

1. Configure `DEBUG=False` no arquivo `.env`
2. Use um servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Configure um proxy reverso (Nginx/Apache)
4. Implemente autenticação de usuários
5. Configure backup automático dos dados

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Entre em contato com o desenvolvedor

## 🔄 Atualizações

Para atualizar o sistema:
```bash
git pull origin main
pip install -r requirements.txt
```
