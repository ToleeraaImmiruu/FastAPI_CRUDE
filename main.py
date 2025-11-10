from fastapi import  Depends ,FastAPI, HTTPException
from schema import PostCreate
from db import session, engine
import db_models
from sqlalchemy.orm import  Session
app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)
text_post = {
    1: {"name": "New Product", "description": "Cool product", "price": 10.5, "quantity": 5},
    2: {"name": "Another Product", "description": "Another cool product", "price": 20.0, "quantity": 10}
}

def get_db():
    db = session()
    yield db 
    db.close()

# saving to the database
def init_db():
    db = session()
    for pro in text_post.values():
        db.add(db_models.Product(**pro))
    db.commit()

init_db()  

# get from the CRUDE

@app.get("/posts")
def get_all_posts(db:Session = Depends(get_db)):

    db_product = db.query(db_models.Product).all()
    return db_product




@app.get("/posts/{id}")
def get_posts_by_id(id: int, db:Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"
    

# post from the CRUDE


@app.post("/posts")
def create_post(post: PostCreate):
    new_post = {"title": post.title,
                "content": post.content, "Year": post.year}
    text_post[max(text_post.keys()) + 1] = new_post
    return new_post

# for the update the product


@app.put("/update/{id}")
def update_product(id: int, pro: PostCreate):
    if id not in text_post:
        raise HTTPException(status_code=404, detail="Post not found")
    # update the existing product
    text_post[id] = {"title": pro.title,
                    "content": pro.content, "year": pro.year}
    
    return {"message": "post updated successfully", "updated_post": text_post[id]}



#  for the delete product 
@app.delete("/delete/{id}")
def delete_product(id:int ):
    if  id not in text_post:
        raise HTTPException(status_code =404,detail="post not found")
    del text_post[id] 
    return { "message":"the product was deleted successfully",}
