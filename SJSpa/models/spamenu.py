from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Spamenus(models.Model):
    id = fields.IntField(pk=True)
    spa_name = fields.CharField(max_length=255,)
    price = fields.FloatField()
    time = fields.CharField(max_length=255)
    description= fields.CharField(max_length=255)

def __str__(self) ->str:
    return self.spa_name

Spamenus_Pydantic = pydantic_model_creator(Spamenus, name="spamenu")
SpamenusIn_Pydantic = pydantic_model_creator(Spamenus, name="spamenu", exclude_readonly=True)