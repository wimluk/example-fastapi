from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import database, models
from .routers import posts, users, auth, votes
from .config import settings

# With alembic, we do not need sqlalchemy to create our tables
# However, we need to upgrade to the desired alembic revision manually
# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"detail": "Hello World"} 