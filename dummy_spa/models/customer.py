from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Customers(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    booking_date = fields.CharField(max_length=255)
    spa_menu = fields.CharField(max_length=255)
    create_at = fields.DatetimeField(auto_now_add=True)

def __str__(self) ->str:
    return self.name

Customers_Pydantic = pydantic_model_creator(Customers, name="Customer")
CustomersIn_Pydantic = pydantic_model_creator(Customers, name="CustomerIn", exclude_readonly=True)