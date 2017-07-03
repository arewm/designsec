import uuid
from django.db import models


# class TagCategory(models.Model):
#     name = models.CharField(max_length=50)
#     help_text = models.CharField(max_length=100)
#     display_order = models.IntegerField(default=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Person(models.Model):
#     expert = models.BooleanField(default=False)
#     person_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     consent_accepted = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#
#
#     def __str__(self):
#         return '{}: expert={}'.format(self.person_id, self.expert)
#
#
# class Tag(models.Model):
#     tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     text = models.CharField(max_length=50)
#     tag_cat = models.ForeignKey(TagCategory, on_delete=models.CASCADE)
#     custom = models.BooleanField(default=False)
#     creator = models.ForeignKey(Person, on_delete=models.CASCADE, default=None, null=True)
#
#     def __str__(self):
#         return '{}: {}'.format(self.tag_cat.name, self.text)
#
#     @property
#     def category(self):
#         return self.tag_cat.name
#
#
# class Action(models.Model):
#     action_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     text = models.CharField(max_length=100)
#
#     def __str__(self):
#         return '{}'.format(self.text)
#
#
# class PolicyAction(models.Model):
#     action_id = models.ForeignKey(Action, on_delete=models.PROTECT)
#     allow = models.BooleanField()
#
#     def __str__(self):
#         return '{}: {}'.format(self.action_id.text, self.allow)
#
#
# class PolicyTag(models.Model):
#     action = models.ForeignKey(Action, on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=None)
#     owner = models.ForeignKey(Person, on_delete=models.CASCADE, default=None)
#     priority = models.IntegerField(default=-1)
#
#     def __str__(self):
#         return '{}: {} = {} ==> {}'.format(self.owner, self.tag, self.action, self.priority)
#
#
# class Policies(models.Model):
#     policy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     tags = models.ManyToManyField(Tag)
#     actions = models.ManyToManyField(PolicyAction)
#     # elements = models.ManyToManyField(PolicyElement)
#     owner = models.ForeignKey(Person, on_delete=models.CASCADE, default=None)
#     time_to_generate = models.FloatField()
#     generated = models.BooleanField(default=False)
#
#     def __str__(self):
#         return ', '.join([str(t) for t in self.tags.all()])

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)

class Recommendation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)

class SecurityList(models.Model):
    name = models.CharField(max_length=100)
    contact = models.EmailField(default=None)
    description = models.TextField(default=None)
    trust = models.TextField(default=None)
    item = models.ManyToManyField(Recommendation)
    visits = models.PositiveIntegerField(default=0)
    last_visit = models.DateTimeField(default=None)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
