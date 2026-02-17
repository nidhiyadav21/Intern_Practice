from fastapi import APIRouter, HTTPException
from app.core.database import categories, transactions, audit_logs
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.schemas.base_schema import APIResponse
from datetime import datetime

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=APIResponse)
async def create_category(data: CategoryCreate):
    doc = data.model_dump()
    doc["name"] = doc["name"].lower()
    doc["created_at"] = datetime.utcnow()
    try:
        await categories.insert_one(doc)
    except:
        raise HTTPException(409, "Category already exists")
    return APIResponse(success=True, message="Created")

@router.get("/", response_model=APIResponse)
async def list_categories():
    result = []
    async for doc in categories.find():
        doc["_id"] = str(doc["_id"])
        result.append(doc)
    return APIResponse(success=True, message="Fetched", data=result)

@router.patch("/{name}", response_model=APIResponse)
async def update_category(name: str, data: CategoryUpdate):
    result = await categories.update_one({"name": name}, {"$set": data.model_dump(exclude_none=True)})
    if result.matched_count == 0:
        raise HTTPException(404, "Category not found")
    return APIResponse(success=True, message="Updated")

@router.delete("/{name}", response_model=APIResponse)
async def delete_category(name: str):
    async with await categories.database.client.start_session() as session:
        async with session.start_transaction():
            category = await categories.find_one({"name": name})
            if not category:
                raise HTTPException(404, "Category not found")

            await categories.delete_one({"name": name})
            await transactions.update_many(
                {"category": name},
                {"$set": {"category": "uncategorized"}}
            )
            await audit_logs.insert_one({
                "action": "delete_category",
                "category": name,
                "timestamp": datetime.utcnow(),
            })

    return APIResponse(success=True, message="Deleted transactionally")