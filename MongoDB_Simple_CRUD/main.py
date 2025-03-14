from fastapi import FastAPI
from pydantic import BaseModel
from MongoDB_Simple_CRUD.config.db_connection import get_db  # Import DB connection

app = FastAPI()
db = get_db()

class Data(BaseModel):
    name:str
    age:int
    dept:str




@app.get("/")
def get_data():
    try:
        collection = db["new_collection"].find()
        data = [
            {
                "name": doc.get("name"),
                "age": doc.get("age"),
                "dept": doc.get("dept")
            } for doc in collection
        ]

        return {"data": data, "status": "successful"}
    except Exception as e:
        return{
            "data":None,
            "message":e,
            "status":"error"
        }

@app.post("/post")
def post_data(data:Data):
    try:
        collection = db["new_collection"].insert_one({
            "name":data.name,
            "age":data.age,
            "dept":data.dept
        })
        return {"data": data, "status": "successful"}
    except Exception as e:
        return{
            "data":None,
            "message":e,
            "status":"error"
        }