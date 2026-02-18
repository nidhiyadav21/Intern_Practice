from fastapi import APIRouter, HTTPException #HTTPException to send error responses (like 404 or 409) to the client.
from app.core.database import categories, transactions, audit_logs
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.schemas.base_schema import APIResponse
from datetime import datetime,timezone

router = APIRouter(prefix="/categories", tags=["Categories"]) #Initializes the router

@router.post("/", response_model=APIResponse)
async def create_category(data: CategoryCreate):
    doc = data.model_dump()       #Converts the Pydantic object into a standard Python dictionary so it can be saved in MongoDB.
    doc["name"] = doc["name"].lower()
    doc["created_at"] = datetime.now(timezone.utc)
    try:
        await categories.insert_one(doc)

        await audit_logs.insert_one({
            "action": "create_category",
            "category": doc["name"],
            "timestamp": datetime.now(timezone.utc)
        })
    except:
        raise HTTPException(409, "Category already exists")
    return APIResponse(success=True, message="Created")

@router.get("/", response_model=APIResponse)
async def list_categories():
    result = []
    async for doc in categories.find():
        doc["_id"] = str(doc["_id"]) #Converts the MongoDB ObjectId to a string
        result.append(doc)
    return APIResponse(success=True, message="Fetched", data=result)

@router.patch("/{name}", response_model=APIResponse)
async def update_category(name: str, data: CategoryUpdate):
    update_data = data.model_dump(exclude_none=True)

    async with await categories.database.client.start_session() as session:
        async with session.start_transaction():
         result = await categories.update_one({"name": name}, {"$set": update_data}, session=session)
         if result.matched_count == 0:
                 raise HTTPException(404, "Category not found")

         await audit_logs.insert_one({
         "action": "update_category",
         "category": name,
         "changes": update_data,
         "timestamp": datetime.now(timezone.utc)
    },    session=session)

    return APIResponse(success=True, message="Updated")


@router.delete("/{name}", response_model=APIResponse)
async def delete_category(name: str):
    async with await categories.database.client.start_session() as session:   #Starts a MongoDB session.
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
                "timestamp": datetime.now(timezone.utc),
            })

    return APIResponse(success=True, message="Deleted transactionally")