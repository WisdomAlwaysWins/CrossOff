from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid
from django.utils import timezone


class User(AbstractUser):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    JOB_ELEMENTARY = 0
    JOB_MIDDLE = 1
    JOB_HIGH = 2
    JOB_UNIV = 3
    JOB_BUSINESS = 4
    JOB_NO = 5
    GENDER_CHOICES = [(GENDER_MALE, '남성'), (GENDER_FEMALE, '여성')]
    JOB_CHOICES = [(JOB_ELEMENTARY, '초등학생'), (JOB_MIDDLE, '중학생'),
                   (JOB_HIGH, '고등학생'), (JOB_UNIV, '대학생'),
                   (JOB_BUSINESS, '직장인'), (JOB_NO, '무직')]
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          unique=True,
                          serialize=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'ID',
        max_length=150,
        unique=True,
        help_text='150자 이내, 영문자, 숫자, @/./+/-/_ 만 사용 가능',
        validators=[username_validator],
        error_messages={
            'unique': "이미 존재하는 ID 입니다.",
        },
    )
    email = models.EmailField(blank=False, null=False)
    nickname = models.CharField(blank=False, null=False, max_length=100)
    birthdate = models.DateField(blank=False, null=False)
    gender = models.IntegerField(choices=GENDER_CHOICES,
                                 blank=False,
                                 null=False,
                                 default=0)
    job = models.IntegerField(choices=JOB_CHOICES,
                              blank=False,
                              null=False,
                              default=5)
    is_manda = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['nickname', 'birthdate', 'email']
