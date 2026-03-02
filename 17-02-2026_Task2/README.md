# 💰 Personal Finance Tracker API

A production-ready Personal Finance Tracker API built using **FastAPI** and **MongoDB (Motor)**.

This API allows users to manage income and expense transactions, categorize them, perform advanced filtering, generate monthly summaries using aggregation pipelines, and execute transactional operations with MongoDB.

The application follows a structured multi-module architecture with proper schema separation, validation, indexing, error handling, and reusable dependencies.

---

## 🚀 Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MongoDB
- **Async Driver:** Motor
- **Validation:** Pydantic v2
- **ODM/Schema Handling:** Native Pydantic + Motor
- **Version Control:** Git
- **API Testing:** Postman

---

# 📁 Project Structure
app/
│
├── main.py
├── core/
│ ├── config.py
│ └── database.py
│
├── models/
│ ├── transaction_models.py
│ └── category_models.py
│
├── schemas/
│ ├── transaction_schema.py
│ └── category_schema.py
│
├── routes/
│ ├── transactions.py
│ └── categories.py
│
├── dependencies/
│ └── pagination.py
│
└── utils/
└── exceptions.py

---

# 🗄 Database Design

## Collections

### 1️⃣ transactions

```json
{
 "_id": "ObjectId",
 "title": "string",
 "description": "string",
 "amount": "float",
 "type": "income | expense",
 "category": "string",
 "date": "datetime",
 "tags": ["string"],
 "created_at": "datetime",
 "updated_at": "datetime"
}
2️⃣ categories
{
 "_id": "ObjectId",
 "name": "string (unique)",
 "type": "income | expense | both",
 "description": "string",
 "created_at": "datetime"
}
3️⃣ audit_logs

Used to log transactional operations when deleting categories.

📌 Indexes (Created Programmatically on Startup)

All indexes are created using Motor during application startup.
| Index                                    | Collection   | Type         | Purpose                      |
| ---------------------------------------- | ------------ | ------------ | ---------------------------- |
| `{ date: -1 }`                           | transactions | Single Field | Chronological listing        |
| `{ category: 1, date: -1 }`              | transactions | Compound     | Filter by category + sort    |
| `{ type: 1, date: -1 }`                  | transactions | Compound     | Filter by type + sort        |
| `{ title: "text", description: "text" }` | transactions | Text         | Full-text search             |
| `{ name: 1 }`                            | categories   | Unique       | Prevent duplicate categories |

🔍 Features Implemented
✅ Transactions

Create transaction

Get transaction by ID

Update transaction (partial update)

Delete transaction

Bulk delete (category/date range)

Advanced filtering with pagination

Full-text search

Monthly summary report (aggregation pipeline)

✅ Categories

Create category

List categories

Update category

Delete category (MongoDB Transaction)

Deletes category

Sets linked transactions to "uncategorized"

Logs operation in audit_logs

Rolls back on failure

📊 Monthly Summary (Aggregation Pipeline)

GET /transactions/summary?month=2024-06

Returns:

Total income

Total expense

Net balance

Category-wise expense breakdown with percentage

Highest expense transaction

🔍 Filtering & Pagination
GET /transactions?category=Food&type=expense&from=2024-06-01&to=2024-06-30&page=1&page_size=20&sort_by=date&order=desc

Supported Query Parameters

category → Filter by category

type → income / expense

from → Start date

to → End date

tags → Must contain all given tags

page → Page number (default: 1)

page_size → Max 100 (default: 20)

sort_by → date or amount

order → asc / desc

Pagination implemented using reusable PaginationParams dependency.

✅ Validation Rules (Pydantic v2)

amount → Must be greater than 0

title → 3–100 characters, trimmed

description → Maximum 500 characters

type → Must be exactly "income" or "expense"

category → Lowercase, not empty

date → Cannot be a future date

tags → Maximum 10 tags, each max 30 characters

page_size → Maximum value 100

Separate request and response schemas are maintained.

⚠ Error Handling

Centralized exception handling

Consistent JSON response structure

Proper HTTP status codes

Custom validation messages

MongoDB transaction rollback on failure

Example Error Response

{
  "success": false,
  "error": "Category not found",
  "status_code": 404
}
▶ Running the Application
Install dependencies
pip install -r requirements.txt
Run server
uvicorn app.main:app --reload
Swagger Documentation
http://localhost:8000/docs

🧠 Design Decisions

Category stored as string for optimized filtering and indexing.

Programmatic index creation ensures portability.

MongoDB transactions ensure data consistency.

Aggregation pipeline used for efficient reporting.

Reusable pagination dependency avoids code duplication.

Strict schema separation improves API clarity.

📌 Conclusion

This project demonstrates:

Advanced FastAPI architecture

MongoDB indexing and aggregation

Transaction handling with rollback

Full-text search

Clean validation with Pydantic v2

Production-level error handling

Developed by Nidhi Yadav
Internship Backend Project – FastAPI & MongoDB

---

If you want, I can now make:

- 🔥 A shorter version for quick GitHub view  
- ⭐ An enterprise-level README with badges & diagrams  
- 📊 A version optimized for recruiters  

Just tell me what you want next 😊







































































































<h1>Personal Finance Tracker API</h1>
 
 Project Overview:-

Personal Finance Tracker is a scalable and modular REST API built using FastAPI and MongoDB to efficiently manage income and expense transactions.
The system is designed with clean architecture principles, asynchronous database operations, structured validation, and real-world financial tracking features such as filtering, bulk operations, and monthly summaries.
This project demonstrates backend development best practices including validation, dependency injection, async programming, and aggregation handling.

**Architecture & Design Approach**
---
The application follows a layered modular architecture:

1)API Layer – Handles routing and HTTP request/response lifecycle.

2)Schema Layer – Data validation using Pydantic models.

3)Core Layer – Configuration and database connection management.

4)Dependency Layer – Reusable dependencies like pagination.

The design ensures:
---
- Separation of concerns.

- Clean and maintainable code.

- Scalable structure for future enhancements.

**Technical Highlights**
---
- Asynchronous API implementation using FastAPI

- Async MongoDB integration via Motor

- Structured request validation using Pydantic

- Dependency Injection for database handling

- MongoDB aggregation for financial summary

- Bulk delete operations with date filtering

- Query-based filtering (category & date range)

- Proper HTTP status codes & exception handling

- Environment-based configuration management

**Internal Request Flow**
---
 1)Client Request: The initial entry point where the user sends data.

 2)FastAPI Router: Receives and directs the request to the appropriate endpoint.

 3)Pydantic Validation: Ensures the incoming data strictly matches the defined schema.

 4)Dependency Injection: Manages and provides required resources, such as database sessions.

 5)Motor (Async MongoDB Driver): Handles the asynchronous connection to the database.

 6)MongoDB Execution: The database performs the requested read or write operation.

 7)Response Serialization: Converts complex Python objects back into a standard format.

 8)Client Receives JSON: The final output is delivered to the user as a JSON payload.

**Core Functionalities**
---

**Category Management**:-
---
- Create category

- View all categories

- Update category

- Delete category

- Duplicate prevention logic

**Transaction Management**:-
---
- Add income/expense transactions

- Update transaction details

- Delete single transaction

- Bulk delete by date range

- Filter by category

- Filter by date range

- Monthly financial summary (Aggregation pipeline)
