from fastapi import FastAPI, HTTPException
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

tasks = [
    {"id": 1, "title":"State Management", "done": False},
    {"id": 2, "title":"API Integration", "done": True},
    {"id": 3, "title":"AI Orchestration", "done": False}
]

class TaskCreated(BaseModel):
    title: str = Field(min_length=1)
    done: bool = Field(default=False)

@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": "[/tasks]"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_tasks_by_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreated):
    title = task.title.strip()
    if title == "":
        raise HTTPException(status_code=400, detail="Title cannot be blank")

    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": task.done}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}")
async def update_task(id: int, update: TaskCreated):
    for task in tasks:
        if task["id"] == id:
            title = update.title.strip()
            if title == "":
                raise HTTPException(status_code=400, detail="Title cannot be blank")
            task["title"] = title
            task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return Response(status_code=204)
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )