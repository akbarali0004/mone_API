from fastapi import FastAPI
from routers import admin_tasks, worker_tasks, stats, login, admin_users, admin_roles
from database import Base, engine

import utils.scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Restaurant Tasks API")

app.include_router(admin_tasks.router)
app.include_router(admin_roles.router)
app.include_router(admin_users.router)
app.include_router(worker_tasks.router)
app.include_router(login.router)
# app.include_router(stats.router)


@app.get("/")
def root():
    return {"ok":True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)