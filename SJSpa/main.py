import jwt

from fastapi import FastAPI, Depends, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from models.customer import Customers, Customers_Pydantic, CustomersIn_Pydantic
from models.spamenu import Spamenus, Spamenus_Pydantic, SpamenusIn_Pydantic
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

app = FastAPI()

JWT_SECRET = 'myjwtsecret'

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name = 'UserIn',exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@app.get('/')
async def root():
    return {'Hello': 'SJSpa'}

@app.post('/token')
async def generate_token(from_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(from_data.username, from_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
    )
  
    user_obj =await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}

async def get_current_uer(token: str =Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
    )

    return await User_Pydantic.from_tortoise_orm(user)

@app.post('/user', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get('/user/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_uer)):
    return user

@app.get('/customer')
async def show_customer():
    return await Customers_Pydantic.from_queryset(Customers.all())
 
@app.get('/spamenu/')
async def show_spamenu():
    return await Spamenus_Pydantic.from_queryset(Spamenus.all())

@app.post('/customer')
async def create_customer(customer: CustomersIn_Pydantic):
    customer_obj = await Customers.create(**customer.dict(exclude_unset=True))
    return await CustomersIn_Pydantic.from_tortoise_orm(customer_obj)

@app.post('/spamenu')
async def create_spamenu(spamenu: SpamenusIn_Pydantic):
    spamenu_obj =await Spamenus.create(**spamenu.dict(exclude_unset=True))
    return await SpamenusIn_Pydantic.from_tortoise_orm(spamenu_obj)

@app.delete('/customer/{id}')
async def delete_customer(id:int):
    customer_count = await Customers.filter(id=id).delete()
    if not customer_count:
        return {'msg': f"Customer {id} not found!"}
    return {'msg': f"Customer {id} delete successful!"}

@app.delete('/spamenu/{id}')
async def deleate_spamenu(id: int):
    spamenu_count = await Spamenus.filter(id=id).delete()
    if not spamenu_count:
        return {'msg': f"Spamenu {id} not found!"}
    return {'msg': f"Spamenu {id} delete successful!"}

@app.put('/customer/{id}')
async def update_customer(id: int, customer: CustomersIn_Pydantic):
    await Customers.filter(id=id).update(**customer.dict(exclude_unset=True))
    return await Customers_Pydantic.from_queryset_single(Customers.get(id=id))

@app.put('/spamenu/{id}')
async def update_spamenu(id: int, spamenu: SpamenusIn_Pydantic):
    await Spamenus.filter(id=id).update(**spamenu.dict(exclude_unset=True))
    return await Spamenus_Pydantic.from_queryset_single(Spamenus.get(id=id))


register_tortoise(
    app,
    db_url='sqlite://db.spa',
    modules={'model': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)
