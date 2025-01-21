import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from views import router

app = FastAPI(title="Grow INVEST")
app.mount("/static", StaticFiles(directory="static/"), name="static")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080)