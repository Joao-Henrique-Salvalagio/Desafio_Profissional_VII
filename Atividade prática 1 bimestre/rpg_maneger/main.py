from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI(title="RPG Manager API")

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.rpg_db

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

class ItemMagicoModel(BaseModel):
    nome: str
    tipo: str
    forca: int
    defesa: int

class PersonagemModel(BaseModel):
    nome: str
    nome_aventureiro: str
    classe: str
    level: int
    forca: int
    defesa: int

def validar_item(data: ItemMagicoModel):
    if data.tipo not in ["Arma", "Armadura", "Amuleto"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")
    if data.forca == 0 and data.defesa == 0:
        raise HTTPException(status_code=400, detail="Item não pode ter 0 de força e defesa")
    if data.tipo == "Arma" and data.defesa != 0:
        raise HTTPException(status_code=400, detail="Armas devem ter defesa igual a 0")
    if data.tipo == "Armadura" and data.forca != 0:
        raise HTTPException(status_code=400, detail="Armaduras devem ter força igual a 0")
    if data.forca > 10 or data.defesa > 10:
        raise HTTPException(status_code=400, detail="Força e defesa máximas são 10")

def validar_personagem(data: PersonagemModel):
    if data.classe not in ["Guerreiro", "Mago", "Arqueiro", "Ladino", "Bardo"]:
        raise HTTPException(status_code=400, detail="Classe inválida")
    if data.forca + data.defesa != 10:
        raise HTTPException(status_code=400, detail="Soma de força e defesa deve ser 10")

@app.post("/personagens")
async def criar_personagem(data: PersonagemModel):
    validar_personagem(data)
    personagem = data.dict()
    personagem["itens"] = []
    res = await db.personagens.insert_one(personagem)
    personagem_salvo = await db.personagens.find_one({"_id": res.inserted_id})
    return {
        "id": str(personagem_salvo["_id"]),
        **{k: personagem_salvo[k] for k in ["nome", "nome_aventureiro", "classe", "level", "forca", "defesa", "itens"]}
    }

@app.get("/personagens")
async def listar_personagens():
    personagens = []
    async for p in db.personagens.find():
        itens = [await db.itens.find_one({"_id": i}) for i in p.get("itens", [])]
        forca_total = p["forca"] + sum(i["forca"] for i in itens if i)
        defesa_total = p["defesa"] + sum(i["defesa"] for i in itens if i)
        personagens.append({
            "id": str(p["_id"]),
            "nome": p["nome"],
            "nome_aventureiro": p["nome_aventureiro"],
            "classe": p["classe"],
            "level": p["level"],
            "forca_total": forca_total,
            "defesa_total": defesa_total,
            "itens": [{**{k: i[k] for k in ["nome", "tipo", "forca", "defesa"]}, "id": str(i["_id"])} for i in itens if i]
        })
    return personagens

@app.get("/personagens/{id}")
async def buscar_personagem(id: str):
    personagem = await db.personagens.find_one({"_id": ObjectId(id)})
    if not personagem:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    itens = [await db.itens.find_one({"_id": i}) for i in personagem.get("itens", [])]
    return {
        "id": str(personagem["_id"]),
        "nome": personagem["nome"],
        "nome_aventureiro": personagem["nome_aventureiro"],
        "classe": personagem["classe"],
        "level": personagem["level"],
        "forca_total": personagem["forca"] + sum(i["forca"] for i in itens if i),
        "defesa_total": personagem["defesa"] + sum(i["defesa"] for i in itens if i),
        "itens": [{**{k: i[k] for k in ["nome", "tipo", "forca", "defesa"]}, "id": str(i["_id"])} for i in itens if i]
    }

@app.put("/personagens/{id}/nome_aventureiro")
async def atualizar_nome_aventureiro(id: str, novo_nome: str):
    result = await db.personagens.update_one({"_id": ObjectId(id)}, {"$set": {"nome_aventureiro": novo_nome}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Personagem não encontrado ou nome igual")
    return {"mensagem": "Nome aventureiro atualizado com sucesso."}

@app.delete("/personagens/{id}")
async def deletar_personagem(id: str):
    await db.personagens.delete_one({"_id": ObjectId(id)})
    return {"mensagem": "Personagem removido com sucesso."}

@app.post("/itens")
async def criar_item(data: ItemMagicoModel):
    validar_item(data)
    item = data.dict()
    res = await db.itens.insert_one(item)
    item_salvo = await db.itens.find_one({"_id": res.inserted_id})
    return {
        "id": str(item_salvo["_id"]),
        **{k: item_salvo[k] for k in ["nome", "tipo", "forca", "defesa"]}
    }

@app.get("/itens")
async def listar_itens():
    itens = []
    async for i in db.itens.find():
        itens.append({**{k: i[k] for k in ["nome", "tipo", "forca", "defesa"]}, "id": str(i["_id"])})
    return itens

@app.get("/itens/{id}")
async def buscar_item(id: str):
    item = await db.itens.find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {**{k: item[k] for k in ["nome", "tipo", "forca", "defesa"]}, "id": str(item["_id"])}

@app.post("/personagens/{id_personagem}/adicionar_item/{id_item}")
async def adicionar_item(id_personagem: str, id_item: str):
    try:
        personagem = await db.personagens.find_one({"_id": ObjectId(id_personagem)})
        item = await db.itens.find_one({"_id": ObjectId(id_item)})
        if not personagem:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")
        if not item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        itens_ids = personagem.get("itens", [])
        if ObjectId(id_item) in itens_ids:
            return {"mensagem": "Item já está atribuído ao personagem."}
        if item["tipo"] == "Amuleto":
            for i_id in itens_ids:
                i = await db.itens.find_one({"_id": i_id})
                if i and i["tipo"] == "Amuleto":
                    raise HTTPException(status_code=400, detail="Personagem já possui um amuleto.")
        await db.personagens.update_one(
            {"_id": ObjectId(id_personagem)},
            {"$push": {"itens": item["_id"]}}
        )
        return {"mensagem": "Item adicionado ao personagem."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/personagens/{id}/amuleto")
async def buscar_amuleto(id: str):
    personagem = await db.personagens.find_one({"_id": ObjectId(id)})
    if not personagem:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    for i_id in personagem.get("itens", []):
        i = await db.itens.find_one({"_id": i_id})
        if i and i["tipo"] == "Amuleto":
            return {**{k: i[k] for k in ["nome", "tipo", "forca", "defesa"]}, "id": str(i["_id"])}
    return {"mensagem": "Nenhum amuleto encontrado."}