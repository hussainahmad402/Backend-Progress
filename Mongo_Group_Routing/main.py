from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from Mongo_Group_Routing.routes.one_database import one_database

app = FastAPI()

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

app.include_router(one_database)
app.include_router(one_database)