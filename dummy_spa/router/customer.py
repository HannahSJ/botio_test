from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix = "/customer",
    tags = ['Customer'],
    responses = {404: {
        'message': "Not found"
        }
    }
)
class Customers(BaseModel):
    name: str
    booking_date: str
    spamenu: str
    price_summary: float
    phone_number: str
    email: str
    description: Optional[str] = None

customer_db = [
     {
            'name': 'Thanit',
            'booking_date': '11/03/2564',
            'spamenu': 'Body Massage',
            'price_summary': 4000.00,
            'phone_number': '0887452699',
            'email': 'ThanitSue@gmail.com',
            'description': 'Love spa mak' 
     },
     {
            'name': 'Tutay',
            'booking_date': '12/03/2564',
            'spamenu': 'Partial Massage',
            'price_summary': 1000.00,
            'phone_number': '0874561522',
            'email': 'Tay@gmail.com',
            'description': 'Tay lay tor' 
     }
 ]

@router.get('')
async def show_all_customer():
     return customer_db

@router.get('/customer/{id}')
async def customer_by_id(id: int):
    customer = customer_db[id-1]
    return customer

@router.post('/customer')
async def create_customer(customer: Customers):
    customer = customer_db.append(customer)
    return customer_db[-1]

@router.delete('/customer/{id}')
async def delete_customer(id: int):
    customer = customer_db[id-1]
    customer_db.pop(id-1)
    result = {'msg', f"{customer['name']} was delete!"}
    return result

@router.put('/customer/{id}')
async def update_spa(id: int, customer: Customers):
    customer_db[id-1].update(**customer.dict())
    result = {'msg': f"Customer id {id} Update successful!!" }
    return result
