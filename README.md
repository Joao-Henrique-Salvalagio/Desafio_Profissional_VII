API desenvolvida para gerenciar **personagens e itens mágicos** em um universo de RPG. O sistema foi criado como parte da atividade prática individual da disciplina de Desafio Profissional VII, seguindo todos os requisitos definidos no enunciado (https://docs.google.com/document/d/1uSSHgEPoulEWfx_GRUBfMDC7UDYNuoGUP_nK42rr1i8/edit?tab=t.0)

---

## Descrição do Projeto

O sistema permite:

- Criar, listar, buscar, atualizar e remover **personagens**
- Criar, listar e buscar **itens mágicos**
- Adicionar/remover itens em personagens
- Respeitar as regras de atributos e restrições de classes e itens mágicos

---

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/rpg-manager-api.git
cd rpg-manager-api
```

### 2. Instale as dependências

```bash
pip install fastapi uvicorn
```

### 3. Execute a API

```bash
uvicorn main:app --reload
```

### 4. Acesse a documentação

Abra no navegador:

```
http://127.0.0.1:8000/docs
```

---

## Funcionalidades Implementadas (Features)

### Personagem
- [x] Cadastrar Personagem (`POST /personagens`)
- [x] Listar Personagens (`GET /personagens`)
- [x] Buscar Personagem por ID (`GET /personagens/{id}`)
- [x] Atualizar Nome Aventureiro (`PUT /personagens/{id}/nome_aventureiro`)
- [x] Remover Personagem (`DELETE /personagens/{id}`)
- [x] Listar Itens Mágicos do Personagem (`GET /personagens/{id}/itens`)
- [x] Buscar Amuleto do Personagem (`GET /personagens/{id}/amuleto`)
- [x] Remover Item do Personagem (`DELETE /personagens/{id}/remover_item/{item_id}`)

### Item Mágico
- [x] Cadastrar Item Mágico (`POST /itens`)
- [x] Listar Itens Mágicos (`GET /itens`)
- [x] Buscar Item Mágico por ID (`GET /itens/{id}`)
- [x] Adicionar Item Mágico ao Personagem (`POST /personagens/{id_personagem}/adicionar_item/{id_item}`)

---

##  Regras e Validações do Sistema

### 🎲 Personagem
- Deve distribuir **10 pontos entre Força e Defesa** (ex: 6-4, 5-5)
- Classes válidas: `Guerreiro`, `Mago`, `Arqueiro`, `Ladino`, `Bardo`
- Os atributos finais **consideram os bônus dos itens mágicos**
- **Apenas 1 amuleto** permitido por personagem

### Item Mágico
- Tipos válidos: `Arma`, `Armadura`, `Amuleto`
- Armas: **Defesa obrigatoriamente 0**
- Armaduras: **Força obrigatoriamente 0**
- Amuletos: Podem ter Força e Defesa (máx. 10 cada)
- Nenhum item pode ter Força e Defesa iguais a 0

---

## Testes

Todos os endpoints podem ser testados via:

- [Postman](https://web.postman.co/)
- Interface Swagger em `http://127.0.0.1:8000/docs`

---

## Autor

**João Henrique Salvalagio Abrahim**  
Estudante de Engenharia de Software – UniCesumar  
Projeto individual desenvolvido para a disciplina de POO

---

## Licença

Uso acadêmico — todos os direitos reservados ao autor.

