from django.db.models import Func


class TrimTrailingZeros(Func):
    function = "trim_scale"
    arity = 1
