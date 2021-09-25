import random
import time

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse


def stream() -> bytes:
    for _ in range(10):
        x = random.random()
        yield f'{x:.5f}\n'.encode()
        print(f'{x:.5f}')
        time.sleep(x)
    print('done')


app = FastAPI()

origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def _stream():
    return StreamingResponse(stream(), media_type='text')


if __name__ == '__main__':
    uvicorn.run(app)
