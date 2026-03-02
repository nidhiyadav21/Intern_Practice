from fastapi import FastAPI
from app.api import transactions,categories
from app.core.database import create_indexes
from app.utils.exceptions import register_exception_handlers

app = FastAPI(title="Personal Finance Tracker")

@app.on_event("startup")
async def startup():
    await create_indexes()

register_exception_handlers(app)

app.include_router(transactions.router)
app.include_router(categories.router)