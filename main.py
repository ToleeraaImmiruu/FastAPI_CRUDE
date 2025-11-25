from fastapi import  Depends ,FastAPI, HTTPException
from schema import PostCreate
from db import session, engine
import db_models
from sqlalchemy.orm import  Session


app = FastAPI()
db_models.Base.metadata.create_all(bind=engine)
text_post = {
    1: {"name": "New Product to db", "description": "Cool product", "price": 10.5, "quantity": 5},
    2: {"name": "Another Product", "description": "Another cool product", "price": 20.0, "quantity": 10}
}

def get_db():
    db = session()
    yield db 
    db.close()
# saving to the database
def init_db():
    db = session() 
    count = db.query(db_models.Product).count
    if count == 0:
        for pro in text_post.values():
            db.add(db_models.Product(**pro))
        db.commit()
init_db()  
# get from the CRUDE

@app.get("/posts")
def get_all_posts(db:Session = Depends(get_db)):

    db_product = db.query(db_models.Product).all()
    db.commit()
    return db_product




@app.get("/posts/{id}")
def get_posts_by_id(id: int, db:Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        return db_product
    db.commit()
    return "product not found"
    


# adding the product to the database 

@app.post("/posts")
def add_product(post: PostCreate, db: Session = Depends(get_db)):
    db.add(db_models.Product(**post.model_dump()))
    db.commit()
    return post

# for the update the product


@app.put("/update/{id}")
def update_product(id: int, pro: PostCreate, db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db_product.name= pro.name
        db_product.description= pro.description
        db_product.price = pro.price
        db_product.quantity = pro.quantity
        db.commit()
        return "product updated {db_product} "

    else:
        return "No product updated "    



#  for the delete product 
@app.delete("/delete/{id}")
def delete_product(id:int , db: Session = Depends(get_db)):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return "The product successfully deleted from the database:{db_product}"
    else:
        return "The product was not exist in the data base"
