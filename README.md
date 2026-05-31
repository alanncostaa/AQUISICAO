# Configuração das Variáveis Globais

Antes da execução do script, é necessário configurar as variáveis globais responsáveis pela autenticação da Meta Graph API e pela conexão com o banco de dados PostgreSQL.

As seguintes variáveis devem ser substituídas pelos valores correspondentes ao ambiente utilizado:

```python
ACCESS_TOKEN = TOKEN_DO_SEU_APP

IG_USER_ID = SEU_IG_ID

BASE_URL = "https://graph.facebook.com/v18.0"

DB_CONFIG = {
    "host": HOST_BANCO,
    "database": DATABASE_BANCO,
    "user": USER_BANCO,
    "password": SENHA_BANCO,
    "port": PORTA_BANCO
}
```

## Descrição das Variáveis

| Variável         | Descrição                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| `ACCESS_TOKEN`   | Token de acesso gerado no Meta for Developers com permissões para consulta dos dados do Instagram. |
| `IG_USER_ID`     | Identificador da conta comercial do Instagram que será monitorada.                                 |
| `HOST_BANCO`     | Endereço do servidor PostgreSQL. Exemplo: `localhost`.                                             |
| `DATABASE_BANCO` | Nome do banco de dados criado para armazenamento dos dados coletados.                              |
| `USER_BANCO`     | Usuário com permissão de acesso ao PostgreSQL.                                                     |
| `SENHA_BANCO`    | Senha do usuário do banco de dados.                                                                |
| `PORTA_BANCO`    | Porta utilizada pelo PostgreSQL. O padrão é `5432`.                                                |

## Exemplo de Configuração

```python
ACCESS_TOKEN = "EAABxxxxxxxxxxxxxxxxxxxx"

IG_USER_ID = "17841400000000000"

BASE_URL = "https://graph.facebook.com/v18.0"

DB_CONFIG = {
    "host": "localhost",
    "database": "instagram_dw",
    "user": "postgres",
    "password": "123456",
    "port": "5432"
}
```

## Pré-requisitos

Antes da execução do script, é necessário:

1. Possuir uma conta comercial do Instagram vinculada a uma Página do Facebook.
2. Criar um aplicativo no Meta for Developers.
3. Gerar um Access Token com as permissões necessárias da Instagram Graph API.
4. Criar previamente o banco de dados PostgreSQL.
5. Executar os scripts de criação das tabelas:

   * `perfil_instagram`
   * `feed_instagram`
   * `metrica_post_instagram`
   * `comentario_instagram`

Após a configuração das variáveis e da estrutura do banco de dados, o script poderá ser executado normalmente para realizar a coleta automática dos dados do Instagram, armazenando informações de perfil, publicações, métricas de desempenho e comentários com análise de sentimento.
