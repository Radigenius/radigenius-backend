from django.db import models

from domain.base import BaseModel
from domain.enums.system.enum import ModelTypes
from domain.apps.system.managers.model_manager import ModelManager
class Model(BaseModel):
    name = models.CharField(max_length=10, choices=ModelTypes.choices)
    description = models.TextField(blank=True)

    objects = ModelManager()

    def __str__(self):
        return self.name
