
# PetVida — Python + SQL Server

## Sobre o projeto

Esse projeto foi desenvolvido para a atividade de Banco de Dados Avançado, utilizando Python, SQL Server e a biblioteca pyodbc.

O objetivo é realizar a conexão com o banco de dados da clínica PetVida e permitir operações de cadastro, consulta, atualização e exclusão de informações.

Como o banco já foi disponibilizado pelo professor, o foco da atividade foi desenvolver as funções em Python para trabalhar com os dados existentes.

## Tecnologias utilizadas

- Python
- SQL Server
- pyodbc
- ODBC Driver 18 for SQL Server
- VS Code

## Estrutura do projeto

- `db.py` — Configuração da conexão com o banco de dados.
- `repositorio.py` — Funções de cadastro, consulta, atualização e exclusão.
- `main.py` — Menu para utilizar as funções pelo terminal.
- `verificar_local.py` — Testes básicos de conexão e consultas.
- `README.md` — Informações sobre o projeto.

## Como executar

Primeiro, é necessário ter o SQL Server instalado e o banco PetVida criado utilizando o script disponibilizado pelo professor.

### 1. Instalar o pyodbc

No terminal, execute:

    pip install pyodbc

### 2. Configurar a conexão

Por padrão, o projeto utiliza:

- Servidor: `.`
- Banco: `PetVida`
- Autenticação: Windows
- Driver: ODBC Driver 18 for SQL Server

Caso necessário, a conexão pode ser configurada pelas variáveis de ambiente:

- `DB_SERVER`
- `DB_NAME`
- `DB_DRIVER`
- `DB_USER`
- `DB_PASSWORD`

### 3. Executar o projeto

Para abrir o menu:

    python main.py

Para executar os testes básicos:

    python verificar_local.py

## Funcionalidades

O projeto foi dividido conforme as etapas da atividade.

### Etapa 1 — Conexão

Conexão entre Python e SQL Server, incluindo o controle de transações.

### Etapa 2 — Tutores

- Cadastrar tutores.
- Buscar tutores pelo ID.
- Listar tutores e filtrar pelo nome.
- Atualizar informações.
- Excluir tutores.

### Etapa 3 — Pets

- Cadastrar pets.
- Atualizar o peso.
- Transferir pets entre tutores.
- Excluir pets.
- Consultar os relacionamentos entre pets e tutores.

### Etapa 4 — Consultas e procedimentos

- Agendar consultas.
- Adicionar e remover procedimentos.
- Listar consultas e procedimentos.
- Calcular o valor total de uma consulta.
- Atualizar o status.
- Excluir consultas.

Também foi incluída a consulta do histórico de atendimentos de um pet.

## Segurança e tratamento de erros

As consultas utilizam parâmetros com `?` para evitar SQL Injection.

Também foram utilizados `commit()` e `rollback()` para controlar as alterações no banco de dados e evitar que operações incompletas sejam salvas.

As conexões são fechadas após a utilização, e os erros são tratados conforme as necessidades das operações.

## Considerações finais

O projeto foi desenvolvido seguindo os conteúdos trabalhados na disciplina e os requisitos apresentados na atividade.

A ideia foi manter o código organizado e utilizar os recursos do Python e do SQL Server para realizar as operações de forma segura.
