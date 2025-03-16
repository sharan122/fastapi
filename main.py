from fastapi import FastAPI
from app.routes import users, auth, rag, rbac

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rag.router)
app.include_router(rbac.router)
@app.get("/")
def root():
    return {"message": "FastAPI JWT Auth is working!"}
