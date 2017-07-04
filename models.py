import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    help_text = models.TextField(default=None)

    def __str__(self):
        return '{}'.format(self.name)

class Classification(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '{}: {}'.format(str(self.category), self.name)

class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    classification = models.ManyToManyField(Classification)

    def __str__(self):
        return '{} --> {}'.format(str(self.classification), self.name)

class Project(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact = models.EmailField(default=None)
    description = models.TextField(default=None)
    trust = models.TextField(default=None)
    item = models.ManyToManyField(Recommendation)
    visits = models.PositiveIntegerField(default=0)
    last_visit = models.DateTimeField(default=None)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'pk:{} name:{}'.format(self.pk, self.name)
