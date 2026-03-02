from fastapi import HTTPException, FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request

def register_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "data": None
            },
        )
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
             status_code=500,
             content={
                "success": False,
                "message": "Internal Server Error",
                 "data": None
             },
        )