import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import task, user, auth, vote
from typing import Dict, List

app = FastAPI(title="Assignment Tracker")

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

allowed_origins: List[str] = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def index() -> Dict[str, str]:
    return {"Welcome": "This is the index page"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)