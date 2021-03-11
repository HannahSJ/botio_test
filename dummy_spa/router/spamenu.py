from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix = "/spamenu",
    tags = ['Spa Menu'],
    responses = { 404: {
        'message': "Not found"
        } 
    }
)

class SpaMenu(BaseModel):
    name: str
    price: float
    time: str
    description: Optional[str] = None

spa_db = [
    {
        'name': 'Body Massage',
        'price': 2000.00,
        'time': '60 mins',
        'description': 'Thai/Aroma'

    },
    {
        'name': 'Partial Massage',
        'price': 1000.00,
        'time': '30 mins',
        'description': 'Head & Shoulder'
    }
]

@router.get('')
async def show_all_spa():
    return spa_db
    
@router.get('/spa/{id}')
async def spa_by_id(id: int):
    spa = spa_db[id - 1]
    return spa

@router.post('/spa')
async def create_spa(spa: SpaMenu):
    spa = spa_db.append(spa)
    return spa_db[-1]

@router.delete('/spa/{id}')
async def delete_spa(id: int):
    spa = spa_db[id-1]
    spa_db.pop(id-1)
    result = {'msg', f"{spa['name']} was delete!"}
    return result

@router.put('/spa/{id}')
async def update_spa(id: int, spa: SpaMenu):
    spa_db[id - 1].update(**spa.dict())
    result = {'msg': f"Spa id {id} Update successful!!"}
    return result
