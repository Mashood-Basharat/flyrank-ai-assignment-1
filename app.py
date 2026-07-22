from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()

tasks = [
    {
        "id": 1,
        "title":"State Management",
        "done": False,
    },
    {
        "id": 2,
        "title":"API Integration",
        "done": True,
    },
    {
        "id": 3,
        "title":"AI Orchestration",
        "done": False,
    }
]

@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": "[/tasks]"
    }

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

@app.get("/health")
async def health():
    return {"status": "ok"}