from pydantic import BaseModel

class Skill(BaseModel):
    id: int = 0
    level: int = 0
    icon: str = ""