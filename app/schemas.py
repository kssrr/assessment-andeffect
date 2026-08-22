from pydantic import BaseModel

class ItemOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}