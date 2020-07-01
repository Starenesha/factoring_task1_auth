from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class Depart(models.Model):
    name_of_depart = models.TextField(max_length=200)
    code_of_depart = models.TextField()

    def __str__(self):
        return "{}".format(self.name_of_depart)


class User(AbstractBaseUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "phone_number"

    first_name = models.CharField('first name', blank=True, null=True, max_length=400)
    last_name = models.CharField('last name', blank=True, null=True, max_length=400)
    password = models.CharField('password', blank=True, null=True, max_length=400)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+399999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True, null=False)  # validators should be a list
    is_active = models.BooleanField('active', default=True)
    is_employee = models.BooleanField('Employer', default=False)
    depart = models.ForeignKey(Depart, on_delete=models.CASCADE, verbose_name="Depart", default="1")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
