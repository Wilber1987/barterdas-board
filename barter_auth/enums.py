from django.db import models


class TokenTypesEnum(models.IntegerChoices):
    VERIFICATION = 1
    RECOVERY_PASSWORD = 2
