from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import os
import time
from datetime import datetime

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _is_updated(request_time):
    """
    Returns if resource is updated or it's the first
    time it has been requested.
    args:
        request_time: last request timestamp
    """
    return os.stat('data.txt').st_mtime > request_time

@app.get("/data-update")
async def get():
    """
    Returns 'data.txt' content when the resource has
    changed after the request time
    """
    request_time = time.time()
    while not _is_updated(request_time):
        time.sleep(0.5)
    content = ''
    with open('data.txt') as data:
        content = data.read()
    return {'content': content, 'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S')}


@app.get("/data")
async def get():
    """
    Returns the current data content
    """
    content = ''
    with open('data.txt') as data:
        content = data.read()
    return {'content': content}

if __name__ == '__main__':
        uvicorn.run(app)