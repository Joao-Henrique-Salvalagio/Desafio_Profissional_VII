# RPG Manager API

API desenvolvida para gerenciar personagens e itens mágicos em um universo de RPG. O sistema foi criado como parte da atividade prática individual da disciplina de **Desafio Profissional VII**, seguindo todos os requisitos definidos no enunciado:  
https://docs.google.com/document/d/1uSSHgEPoulEWfx_GRUBfMDC7UDYNuoGUP_nK42rr1i8/edit?tab=t.0

---

## Descrição do Projeto

O sistema permite:

- Criar, listar, buscar, atualizar e remover personagens
- Criar, listar e buscar itens mágicos
- Adicionar/remover itens a personagens
- Respeitar regras de atributos e restrições de classes e itens
- Armazenar todos os dados no **MongoDB**

---

## 🚀 Como executar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/rpg-manager-api.git
cd rpg-manager-api
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```
> Ou manualmente:
```bash
pip install fastapi uvicorn motor python-dotenv
```

### 3. Configure o MongoDB

O projeto utiliza o **MongoDB local**, rodando na porta padrão `27017`. Certifique-se de:

- Ter o **MongoDB instalado** no seu sistema: https://www.mongodb.com/try/download/community
- O **serviço do MongoDB esteja ativo** antes de executar a API
- O banco de dados usado é `rpg_db`, e será criado automaticamente ao rodar a aplicação

Se quiser alterar a URL de conexão, modifique diretamente esta linha no código:
```python
client = AsyncIOMotorClient("mongodb://localhost:27017")
```

### 4. Execute a API
```bash
uvicorn main:app --reload
```

### 5. Acesse a documentação interativa
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Funcionalidades Implementadas (Features)

### Personagem
- Cadastrar Personagem (`POST /personagens`)
- Listar Personagens (`GET /personagens`)
- Buscar Personagem por ID (`GET /personagens/{id}`)
- Atualizar Nome Aventureiro (`PUT /personagens/{id}/nome_aventureiro?novo_nome=XXX`)
- Remover Personagem (`DELETE /personagens/{id}`)
- Listar Itens do Personagem (`GET /personagens/{id}/itens`)
- Buscar Amuleto do Personagem (`GET /personagens/{id}/amuleto`)
- Remover Item do Personagem (`DELETE /personagens/{id}/remover_item/{item_id}`)

### Item Mágico
- Cadastrar Item Mágico (`POST /itens`)
- Listar Itens Mágicos (`GET /itens`)
- Buscar Item por ID (`GET /itens/{id}`)
- Adicionar Item ao Personagem (`POST /personagens/{id_personagem}/adicionar_item/{id_item}`)

---

## Regras e Validações do Sistema

### Personagem
- Deve distribuir exatamente 10 pontos entre Força e Defesa (ex: 6-4, 7-3)
- Classes válidas: `Guerreiro`, `Mago`, `Arqueiro`, `Ladino`, `Bardo`
- Os atributos finais consideram os bônus dos itens mágicos
- Um personagem pode ter apenas **1 Amuleto**

### Item Mágico
- Tipos permitidos: `Arma`, `Armadura`, `Amuleto`
- `Arma`: Defesa obrigatoriamente 0
- `Armadura`: Força obrigatoriamente 0
- `Amuleto`: Pode ter Força e Defesa, máximo de 10 cada
- Nenhum item pode ter Força e Defesa ambos zerados

---

## Testes da API

Todos os endpoints podem ser testados via:

- [Postman](https://www.postman.com/)
- Interface Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Autor

**João Henrique Salvalagio Abrahim**  
Estudante de Engenharia de Software – UniCesumar  
Projeto individual desenvolvido para a disciplina de **POO**

---

## Licença

Uso estritamente **acadêmico**. Todos os direitos reservados ao autor.
