import datetime

from django.db import models

# Create your models here.


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        return super().get_queryset()


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
