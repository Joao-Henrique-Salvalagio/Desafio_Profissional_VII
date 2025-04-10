from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI(title="RPG Manager API")

# ==========================
# MODELOS DE ENTRADA
# ==========================

class ItemMagicoModel(BaseModel):
    nome: str
    tipo: str  # Arma, Armadura, Amuleto
    forca: int
    defesa: int

class PersonagemModel(BaseModel):
    nome: str
    nome_aventureiro: str
    classe: str  # Guerreiro, Mago, Arqueiro, Ladino, Bardo
    level: int
    forca: int
    defesa: int

# ==========================
# ENTIDADES
# ==========================

class ItemMagico:
    def __init__(self, id, nome, tipo, forca, defesa):
        if tipo not in ["Arma", "Armadura", "Amuleto"]:
            raise ValueError("Tipo inválido.")
        if forca == 0 and defesa == 0:
            raise ValueError("Item não pode ter 0 de força e 0 de defesa.")
        if tipo == "Arma" and defesa != 0:
            raise ValueError("Armas devem ter defesa igual a 0.")
        if tipo == "Armadura" and forca != 0:
            raise ValueError("Armaduras devem ter força igual a 0.")
        if forca > 10 or defesa > 10:
            raise ValueError("Força e defesa devem ser no máximo 10.")

        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.forca = forca
        self.defesa = defesa

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "forca": self.forca,
            "defesa": self.defesa
        }

class Personagem:
    def __init__(self, id, nome, nome_aventureiro, classe, level, forca, defesa):
        if classe not in ["Guerreiro", "Mago", "Arqueiro", "Ladino", "Bardo"]:
            raise ValueError("Classe inválida.")
        if forca + defesa != 10:
            raise ValueError("A soma entre força e defesa deve ser exatamente 10.")

        self.id = id
        self.nome = nome
        self.nome_aventureiro = nome_aventureiro
        self.classe = classe
        self.level = level
        self.base_forca = forca
        self.base_defesa = defesa
        self.itens: List[ItemMagico] = []

    def adicionar_item(self, item: ItemMagico):
        if item.tipo == "Amuleto" and any(i.tipo == "Amuleto" for i in self.itens):
            raise ValueError("Já possui um amuleto.")
        self.itens.append(item)

    def remover_item(self, item_id: str):
        self.itens = [item for item in self.itens if item.id != item_id]

    def buscar_amuleto(self):
        return next((item for item in self.itens if item.tipo == "Amuleto"), None)

    def forca_total(self):
        return self.base_forca + sum(i.forca for i in self.itens)

    def defesa_total(self):
        return self.base_defesa + sum(i.defesa for i in self.itens)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "nome_aventureiro": self.nome_aventureiro,
            "classe": self.classe,
            "level": self.level,
            "forca_total": self.forca_total(),
            "defesa_total": self.defesa_total(),
            "itens": [i.to_dict() for i in self.itens]
        }

# ==========================
# BANCOS EM MEMÓRIA
# ==========================

personagens = {}
itens = {}

# ==========================
# ROTAS PERSONAGEM
# ==========================

@app.post("/personagens")
def criar_personagem(data: PersonagemModel):
    id = str(uuid.uuid4())
    personagem = Personagem(id, data.nome, data.nome_aventureiro, data.classe, data.level, data.forca, data.defesa)
    personagens[id] = personagem
    return personagem.to_dict()

@app.get("/personagens")
def listar_personagens():
    return [p.to_dict() for p in personagens.values()]

@app.get("/personagens/{id}")
def buscar_personagem(id: str):
    if id not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return personagens[id].to_dict()

@app.put("/personagens/{id}/nome_aventureiro")
def atualizar_nome_aventureiro(id: str, novo_nome: str):
    if id not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    personagens[id].nome_aventureiro = novo_nome
    return {"mensagem": "Nome aventureiro atualizado com sucesso."}

@app.delete("/personagens/{id}")
def deletar_personagem(id: str):
    if id not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    del personagens[id]
    return {"mensagem": "Personagem removido com sucesso."}

@app.get("/personagens/{id}/itens")
def listar_itens_personagem(id: str):
    if id not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    return personagens[id].to_dict()["itens"]

@app.get("/personagens/{id}/amuleto")
def buscar_amuleto_personagem(id: str):
    if id not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    amuleto = personagens[id].buscar_amuleto()
    if not amuleto:
        return {"mensagem": "Personagem não possui amuleto."}
    return amuleto.to_dict()

@app.delete("/personagens/{id}/remover_item/{item_id}")
def remover_item_personagem(id: str, item_id: str):
    if id not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    personagens[id].remover_item(item_id)
    return {"mensagem": "Item removido do personagem."}

# ==========================
# ROTAS ITEM MÁGICO
# ==========================

@app.post("/itens")
def criar_item(data: ItemMagicoModel):
    id = str(uuid.uuid4())
    try:
        item = ItemMagico(id, data.nome, data.tipo, data.forca, data.defesa)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    itens[id] = item
    return item.to_dict()

@app.get("/itens")
def listar_itens():
    return [i.to_dict() for i in itens.values()]

@app.get("/itens/{id}")
def buscar_item(id: str):
    if id not in itens:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return itens[id].to_dict()

@app.post("/personagens/{id_personagem}/adicionar_item/{id_item}")
def adicionar_item_ao_personagem(id_personagem: str, id_item: str):
    if id_personagem not in personagens:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    if id_item not in itens:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    try:
        personagens[id_personagem].adicionar_item(itens[id_item])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return personagens[id_personagem].to_dict()
