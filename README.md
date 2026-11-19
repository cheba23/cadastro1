# 📦 Sistema de Cadastro de Produtos

Sistema web desenvolvido com **Python e Flask** para gerenciamento de produtos e categorias. O projeto permite cadastrar, consultar, editar e excluir produtos, com suporte ao envio de imagens.

## 🚀 Funcionalidades

- [x] Cadastro de produtos
- [x] Cadastro de preços
- [x] Associação de produtos com categorias
- [x] Upload de imagens
- [x] Listagem de produtos
- [x] Pesquisa de produtos pelo nome
- [x] Edição de produtos cadastrados
- [x] Exclusão de produtos
- [x] Exibição de mensagens de sucesso e erro

## 🛠️ Tecnologias utilizadas

- **Python** – Linguagem principal
- **Flask** – Framework web
- **Flask-SQLAlchemy / SQLAlchemy** – Integração com banco de dados
- **HTML5** – Estrutura das páginas
- **CSS3** – Estilização
- **SQLite** – Banco de dados

## 📁 Estrutura do projeto

```text
projeto/
│
├── static/
│   ├── css/
│   │   └── produtos.css
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── editar_produto.html
│
├── routes/
│
├── models.py
├── db.py
├── app.py
├── requirements.txt
└── .gitignore
```

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Entre na pasta do projeto

```bash
cd nome-do-projeto
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a aplicação

```bash
python app.py
```

### 7. Acesse no navegador

```text
http://127.0.0.1:5000
```

## 📌 Objetivo do projeto

O objetivo deste projeto é desenvolver uma aplicação web utilizando Flask, praticando conceitos de desenvolvimento backend, integração com banco de dados, operações CRUD e organização de aplicações web.

## 👨‍💻 Desenvolvido com

Python + Flask ❤️