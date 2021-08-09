import datetime

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

# Create your models here.


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        return super().get_queryset()


class UserManagerUpdate(UserManager):

    def create(self, **kwargs):
        return super().create(username=kwargs['phone'], **kwargs)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_superuser(username, email, password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'phone'
    objects = UserManagerUpdate()
    phone = models.CharField(max_length=13, unique=True)


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    create_time_stamp = models.DateTimeField(auto_now_add=True)
    modify_time_stamp = models.DateTimeField(auto_now=True)
    delete_time_stamp = models.DateTimeField(default=None, null=True, blank=True)

    def logical_delete(self):
        self.delete_time_stamp = datetime.datetime.now()
        self.save()

    # def is_deleted(self):
    #     query = TimeStampMixin.objects.order_by('delete_time_stamp')
    #     if query:
    #         return True
    #     else:
    #         return False


class BaseModel(TimeStampMixin):

    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    objects = BaseManager()
    indexes = [
        models.Index(fields=['deleted'])
    ]


class BaseTest(BaseModel):
    pass
