from pydantic import BaseModel

# Model Pydantic = Datatype
class Member(BaseModel):
    id: str
    nom: str
    prenom: str
    email: str
    telephone: str

class MemberCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    telephone: str

class User(BaseModel):
    email: str
    password: str
