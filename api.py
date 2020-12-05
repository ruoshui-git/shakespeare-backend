from generate import generate_in_play, generate, ModelOut
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:5000",
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins)
]

app = FastAPI(middleware=middleware)


@app.get('/')
async def index():
    return {'message': 'Up and and running!'}


app.get('/generate/raw', response_model=ModelOut)(generate)

app.get('/generate', response_model=ModelOut)(generate_in_play)
