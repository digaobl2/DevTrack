from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

engine = create_engine("sqlite:///./devtrack.db")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class VagaDB(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True)
    empresa = Column(String)
    cargo = Column(String)


Base.metadata.create_all(bind=engine)


class Vaga(BaseModel):
    empresa: str
    cargo: str


@app.get("/")
def home():
    return {"message": "DevTrack API funcionando!"}


@app.post("/vagas")
def criar_vaga(vaga: Vaga):

    db = SessionLocal()

    nova_vaga = VagaDB(
        empresa=vaga.empresa,
        cargo=vaga.cargo
    )

    db.add(nova_vaga)
    db.commit()
    db.refresh(nova_vaga)
    db.close()

    return nova_vaga

@app.get("/vagas")
def listar_vagas():
    db = SessionLocal()
    vagas = db.query(VagaDB).all()
    db.close()

    return vagas

@app.delete("/vagas/{vaga_id}")
def deletar_vaga(vaga_id: int):

    db = SessionLocal()

    vaga = db.query(VagaDB).filter(VagaDB.id == vaga_id).first()

    if not vaga:
        db.close()
        return {"erro": "Vaga não encontrada"}

    db.delete(vaga)
    db.commit()
    db.close()

    return {"mensagem": "Vaga deletada!"}
@app.put("/vagas/{vaga_id}")
def atualizar_vaga(vaga_id: int, vaga: Vaga):
    db = SessionLocal()

    vaga_db = db.query(VagaDB).filter(VagaDB.id == vaga_id).first()

    if not vaga_db:
        db.close()
        return {"erro": "Vaga não encontrada"}

    vaga_db.empresa = vaga.empresa
    vaga_db.cargo = vaga.cargo

    db.commit()
    db.refresh(vaga_db)
    db.close()

    return vaga_db