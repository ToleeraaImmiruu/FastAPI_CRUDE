

from pydantic import BaseModel
 
class PostCreate(BaseModel):
  name: str 
  description: str
  price: float
  quantity: int   
  
