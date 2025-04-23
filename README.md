# 🏆 Projeto Clash Royale

Projeto desenvolvido para a disciplina de **Banco de Dados Não Convencionais**, com foco em exploração e análise de dados utilizando **MongoDB** e **Streamlit**.

---

## 💻 Tecnologias Utilizadas

- **Python** – linguagem principal do projeto
- **MongoDB** – banco de dados NoSQL utilizado
- **PyMongo** – driver para integração Python ↔ MongoDB
- **Clash Royale API (Supercell)** – obtenção dos dados de batalhas, jogadores e cartas
- **Streamlit** – construção da interface interativa para visualização das consultas

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/Projeto-Clash-Royale.git
cd Projeto-Clash-Royale
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
MONGOKEY=<sua_string_de_conexao_mongodb>
API_KEY=<sua_clash_royale_api_key>
```

### 5. Execute a interface com Streamlit
```bash
streamlit run stfront.py
```

A aplicação abrirá automaticamente no seu navegador padrão.

---

## 📊 Funcionalidades disponíveis

- Consultas interativas sobre cartas, decks e jogadores
- Filtros por data, porcentagem e seleção de combos de cartas
- Cálculo e exibição de estatísticas como win rate, taxa de uso, número de vitórias/derrotas
- Visualização limpa e amigável utilizando Streamlit

---

## 👥 Grupo

- **Gabriel Vieira**
- **Juliana Moreira**
- **Vitor Robemar**

---

## 🛠️ Contribuições

- Interface Web desenvolvida com **Streamlit**
- Refatoração de código e organização das consultas
- Integração dos filtros com as queries MongoDB

---

## 📚 Licença

Este projeto é apenas para fins **educacionais** e acadêmicos.

