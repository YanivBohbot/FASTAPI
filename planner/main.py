from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.events import event_router
import uvicorn
from database.connections import Settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

settings = Settings()

# register origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.on_event("startup")
async def init_db():
    await Settings.initialize_database()


@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
