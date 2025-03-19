from django.db import models
from django.core.validators import MinValueValidator


class MoneyField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 19)
        kwargs.setdefault("decimal_places", 2)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_digits") == 19:
            del kwargs["max_digits"]
        if kwargs.get("decimal_places") == 2:
            del kwargs["decimal_places"]
        return name, path, args, kwargs


class PercentField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_digits", 2)
        kwargs.setdefault("decimal_places", 0)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_digits") == 2:
            del kwargs["max_digits"]
        if kwargs.get("decimal_places") == 0:
            del kwargs["decimal_places"]
        return name, path, args, kwargs


class PositivePercentField(PercentField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.get("validators", [])
        validators.append(MinValueValidator(0))
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if "validators" in kwargs:
            kwargs["validators"] = [
                validator
                for validator in kwargs["validators"]
                if not isinstance(validator, MinValueValidator)
            ]
            if not kwargs["validators"]:
                del kwargs["validators"]
        return name, path, args, kwargs
