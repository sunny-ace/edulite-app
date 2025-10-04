# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI(title ="Edutrack Lite API")

# @app.get("/")
# def root():
#     return {"message": "Hello, FastAPI!"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool = None


# @app.post("/items/")
# def create_item(item: Item):
#     return {"item_name": item.name, "item_price": item.price, "is_offer": item.is_offer}

# from fastapi import FastAPI
# from routes import user_routes, course, enrollment 

# app = FastAPI()

# # include the user routes
# app.include_router(user_routes.router)
# app.include_router(course.router)
# app.include_router(enrollment.router)
# main.py
from fastapi import FastAPI
from routes import user_routes, course, enrollment

app = FastAPI(title="EduLight API")

app.include_router(user_routes.router)
app.include_router(course.router)
app.include_router(enrollment.router)

