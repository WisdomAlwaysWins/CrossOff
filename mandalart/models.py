from django.db import models
from common.models import User
import uuid


class Mandalart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)

    def __str__(self):
        return str(self.user.nickname) + '의 만다라트'


class BigGoal(models.Model):
    manda = models.OneToOneField(Mandalart,
                                 on_delete=models.CASCADE,
                                 primary_key=True)
    content = models.CharField(max_length=200)
    is_achieved = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.manda.user.nickname) + '의 큰 목표 ' + str(self.content)


class MidGoal(models.Model):
    big = models.ForeignKey(BigGoal,
                            on_delete=models.CASCADE,
                            related_name='midgoal')
    content = models.CharField(max_length=200)
    is_achieved = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.big.manda.user.nickname) + '의 ' + str(self.content)


class SpecificGoal(models.Model):
    mid = models.ForeignKey(MidGoal,
                            on_delete=models.CASCADE,
                            related_name='specificgoal')
    content = models.CharField(max_length=200)
    is_achieved = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.mid.big.manda.user.nickname) + '의 ' + str(self.content)


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo')
    content = models.CharField(max_length=200, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_achieved = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.user.nickname) + '의 ' + str(self.content)


class BlockManager(models.Manager):
    def get_by_natural_key(self, user):
        pass


class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block')
    content = models.TextField()
    date = models.DateField(auto_now_add=False, null=False)

    def __str__(self):
        return str(self.user.nickname) + '의 ' + str(self.date) + '날짜의 ' + str(self.content[:10])


class Spelist(models.Model):
    id = models.BigAutoField(primary_key=True)
    block = models.OneToOneField(Block, on_delete=models.CASCADE, related_name='spelist')

    def __str__(self):
        return str(self.block.user.nickname) + '의 ' + str(self.block.date) + ' 날짜의 세부목표 목록'


class Item(models.Model):
    spelist = models.ForeignKey(Spelist, on_delete=models.CASCADE, related_name='item')
    specificgoal = models.ForeignKey(SpecificGoal, on_delete=models.CASCADE, related_name='specificgoal')

    def __str__(self) -> str:
        return str(self.spelist.block.user.nickname) + '의 ' + str(self.spelist.block.date) + ' 날짜의 ' + str(self.specificgoal.content)
