from fastapi import FastAPI,Request
from pydantic import BaseModel
from bson import ObjectId   
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from MongoDB_Simple_CRUD.config.db_connection import get_db  # Import DB connection

app = FastAPI()
db = get_db()

class Data(BaseModel):
    name:str
    age:int
    dept:str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(map(str, error["loc"])),  # Converts tuple path to a string
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }
    )



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
    
@app.put("/update/{id}")
def updata_data(id:str , data:Data):
    try:
        existing_data=db["new_collection"].find_one({"_id":ObjectId(id)})
        if not existing_data:
            return{
                "status":"error",
                "message":"Document not found"
            }
        updated_data = {
            "name":data.name if data.name is not None else existing_data["name"],
            "age":data.age if data.age is not None else existing_data["age"],
            "dept":data.dept if data.dept is not None else existing_data["dept"]
        }

        db["new_collection"].update_one(
            {"_id":ObjectId(id)},
            {"$set":updated_data}
        )
        return{
            "status":"Data Updated successfully"
        }


    except Exception as e:
        return {
            "data":None,
            "message":e,
            "status":"error"
        }

@app.delete("/delete/{id}")
def delete_data(id: str):
    try:
        db.new_collection.delete_one({"_id": ObjectId(id)})
        return {
            "status": "Data Deleted Successfully"
        }
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }
