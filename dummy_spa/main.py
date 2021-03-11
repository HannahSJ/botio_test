from fastapi import FastAPI
from pydantic import BaseModel
from router import spamenu, customer


app = FastAPI()

app.include_router(spamenu.router)
app.include_router(customer.router)

@app.get('/')
async def root():
    return {'Hello': 'SJ SPA'}

    