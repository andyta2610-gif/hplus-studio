from pydantic import BaseModel

class CustomerDesignRequest(BaseModel):
    room: str
    area: float
    style: str
    budget: str
