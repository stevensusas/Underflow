from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()


app = FastAPI()


@app.get("/")
async def root():
    return {"data": "Stack Underflow"}


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000)
