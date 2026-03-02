from fastapi import APIRouter, Depends, HTTPException, Query  #Depends - Used to inject the reusable Pagination logic.
from app.core.database import transactions,audit_logs
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate
from app.schemas.base_schema import APIResponse
from app.dependencies.pagination import PaginationParams
from bson import ObjectId  #ObjectId: MongoDB IDs are special objects; we need this to convert the string ID from the URL into a format MongoDB understands.
from datetime import datetime,timezone

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def serialize(doc):     #A helper function that converts the MongoDB _id (an object) into a string so it can be sent as JSON.
    doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=APIResponse)
async def create_transaction(data: TransactionCreate):
    doc = data.model_dump()
    doc["created_at"] = datetime.now(timezone.utc)
    doc["updated_at"] = datetime.now(timezone.utc)

    result = await transactions.insert_one(doc)
    transaction_id = str(result.inserted_id)

    # 1. Log the Creation
    await audit_logs.insert_one({
        "action": "create_transaction",
        "transaction_id": transaction_id,
        "amount": doc["amount"],
        "timestamp": datetime.now(timezone.utc)
    })

    return APIResponse(success=True, message="Created", data={"id": transaction_id})

@router.get("/", response_model=APIResponse)
async def list_transactions(
    category: str | None = None,
    type: str | None = None,
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    tags: list[str] | None = Query(None),
    sort_by: str = "date",
    order: str = "desc",
    pagination: PaginationParams = Depends(),
):
    query = {}

    if category: query["category"] = category
    if type: query["type"] = type
    if from_date and to_date:
        query["date"] = {"$gte": from_date, "$lte": to_date}
    if tags:
        query["tags"] = {"$all": tags}

    sort_direction = -1 if order == "desc" else 1

    cursor = transactions.find(query)\
        .sort(sort_by, sort_direction)\
        .skip(pagination.skip)\
        .limit(pagination.page_size)

    results = [serialize(doc) async for doc in cursor]

    return APIResponse(success=True, message="Fetched", data=results)

@router.get("/search", response_model=APIResponse)
async def search_transactions(q: str):
    cursor = transactions.find({"$text": {"$search": q}})
    results = [serialize(doc) async for doc in cursor]
    return APIResponse(success=True, message="Search results", data=results)


@router.get("/summary", response_model=APIResponse)
async def summary(month: str):
    try:
        year, month_val = map(int, month.split("-"))  # Changed variable name to avoid shadowing
    except ValueError:
        raise HTTPException(400, "Invalid month format. Use YYYY-MM")

    pipeline = [
        {"$match": {
            "$expr": {
                "$and": [
                    {"$eq": [{"$year": "$date"}, year]},
                    {"$eq": [{"$month": "$date"}, month_val]},
                ]
            }
        }},
        {"$facet": {
            "totals": [
                {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}}
            ],
            "highest_expense": [
                {"$match": {"type": "expense"}},
                {"$sort": {"amount": -1}},
                {"$limit": 1}
            ],
            "category_breakdown": [
                {"$match": {"type": "expense"}},
                {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
            ]
        }}
    ]

    # 1. Get the list (facet always returns a list with 1 document)
    raw_result = await transactions.aggregate(pipeline).to_list(length=1)

    if not raw_result:
        return APIResponse(success=True, message="No data found", data={})

    # 2. Extract the actual facet object
    data = raw_result[0]

    # 3. Serialize the ONLY part that contains an ObjectId (highest_expense)
    if data.get("highest_expense"):
        data["highest_expense"] = [serialize(doc) for doc in data["highest_expense"]]

    return APIResponse(success=True, message="Summary", data=data)


@router.get("/{id}", response_model=APIResponse)
async def get_transaction(id: str):
    doc = await transactions.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(404, "Transaction not found")
    return APIResponse(success=True, message="Fetched", data=serialize(doc))


@router.patch("/{id}", response_model=APIResponse)
async def update_transaction(id: str, data: TransactionUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)

    async with await transactions.database.client.start_session() as session:
        async with session.start_transaction():
            result = await transactions.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data},
                session=session
            )

            if result.matched_count == 0:
                raise HTTPException(404, "Transaction not found")

            # 2. Log the Update
            await audit_logs.insert_one({
                "action": "update_transaction",
                "transaction_id": id,
                "changes": update_data,
                "timestamp": datetime.now(timezone.utc)
            }, session=session)

    return APIResponse(success=True, message="Updated")


@router.delete("/bulk", response_model=APIResponse)
async def bulk_delete(category: str | None = None):
    query = {}
    if category: query["category"] = category

    async with await transactions.database.client.start_session() as session:
        async with session.start_transaction():
            result = await transactions.delete_many(query, session=session)

            # 3. Log the Bulk Delete
            await audit_logs.insert_one({
                "action": "bulk_delete_transactions",
                "filter": query,
                "count": result.deleted_count,
                "timestamp": datetime.now(timezone.utc)
            }, session=session)

    return APIResponse(success=True, message="Bulk deleted", data={"count": result.deleted_count})


@router.delete("/{id}", response_model=APIResponse)
async def delete_transaction(id: str):
    async with await transactions.database.client.start_session() as session:
        async with session.start_transaction():
            result = await transactions.delete_one({"_id": ObjectId(id)}, session=session)

            if result.deleted_count == 0:
                raise HTTPException(404, "Transaction not found")

            # 4. Log the Single Delete
            await audit_logs.insert_one({
                "action": "delete_transaction",
                "transaction_id": id,
                "timestamp": datetime.now(timezone.utc)
            }, session=session)

    return APIResponse(success=True, message="Deleted")


