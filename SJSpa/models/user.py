from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    @classmethod
    async def get_login(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return True

    User_Pydantic = pydantic_model_creator(User, name="User")
    UserIn_Pydantic = pydantic_model_creator(User, name = 'UserIn',exclude_readonly=True)