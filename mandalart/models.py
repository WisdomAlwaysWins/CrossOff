from django.db import models
from common.models import User
import uuid


class Mandalart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)


class BigGoal(models.Model):
    manda = models.OneToOneField(Mandalart,
                                 on_delete=models.CASCADE,
                                 primary_key=True)
    content = models.CharField(max_length=200)


class MidGoal(models.Model):
    big = models.ForeignKey(BigGoal,
                            on_delete=models.CASCADE,
                            related_name='biggoal')
    content = models.CharField(max_length=200)


class SpecificGoal(models.Model):
    mid = models.ForeignKey(MidGoal,
                            on_delete=models.CASCADE,
                            related_name='midgoal')
    content = models.CharField(max_length=200)
