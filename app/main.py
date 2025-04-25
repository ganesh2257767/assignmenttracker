import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import task, user, auth, vote

app = FastAPI(title="TaskBook")

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)