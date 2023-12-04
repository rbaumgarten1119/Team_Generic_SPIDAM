from fastapi import FastAPI
from Model import Audio

app = FastAPI


@app.get("/audio")
async def get_audio():
    return
