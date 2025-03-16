from fastapi import APIRouter
from bson import ObjectId
from Mongo_Group_Routing.config.db_connection import get_db

one_database=APIRouter(prefix="/one",tags=["first"])
db=get_db()

@one_database.get("/")
async def get_data():
    try:
        collection=db.new_collection.find()
        print("reached here successfuly")
        data = [
            {
                "name": doc.get("name"),
                "age": doc.get("age"),
                "dept": doc.get("dept")
            } for doc in collection
        ]

        return {
            "data": data, 
            "status": "successful"
            }


    except Exception as e:
        return{
            "data":None,
            "message":str(e),
            "status":"error"
        } 