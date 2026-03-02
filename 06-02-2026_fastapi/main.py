import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel


app = FastAPI()

class Task(BaseModel):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False



db = []
id_counter = 1

#GET
@app.get("/tasks")
async def get_tasks():
    return {"all tasks":db}

#CREATE
@app.post("/tasks")
async def create_tasks(task: Task):
    global id_counter
    task.id = id_counter
    db.append(task.dict())
    id_counter += 1
    return {"message": "Task Added!","data": task}


#Update
@app.put("/tasks/{task_id}")
async def update_tasks(task_id: int, updated_tasks: Task):
    for index, task in enumerate(db):
        if task["id"] == task_id:
            updated_tasks.id = task_id
            db[index] = updated_tasks.dict()   #convert to dict
            return {"message": "Task Updated!", "data": db[index]}
    raise HTTPException(status_code=404, detail="Task not found")


#Delete
@app.delete("/tasks/{task_id}")
async def delete_tasks(task_id: int):
    for index,task in enumerate(db):
        if task["id"] == task_id:
           delete_item = db.pop(index)
           return {"message": f"Task Deleted!: {delete_item['title']}"}
        raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
         host="127.0.0.1",
         port=8000,
         reload=True,)

