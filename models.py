import uuid
from urllib.parse import quote
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from bleach import clean, ALLOWED_TAGS, ALLOWED_ATTRIBUTES, ALLOWED_STYLES

# #: List of allowed tags
# ALLOWED_TAGS = [
#     'a',
#     'abbr',
#     'acronym',
#     'b',
#     'blockquote',
#     'code',
#     'em',
#     'i',
#     'li',
#     'ol',
#     'strong',
#     'ul',
# ]
#
#
# #: Map of allowed attributes by tag
# ALLOWED_ATTRIBUTES = {
#     'a': ['href', 'title'],
#     'abbr': ['title'],
#     'acronym': ['title'],
# }
#
#
# #: List of allowed styles
# ALLOWED_STYLES = []

# Add to the beach.clean whitelist settings
ALLOWED_TAGS.extend(['p', 'sup', 'sub', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'])
ALLOWED_ATTRIBUTES.update({
    'p' : ['style'],
    'span' : ['style']
})
ALLOWED_STYLES.extend(['padding-left', 'text-decoration', 'text-align'])



class Category(models.Model):
    """
    A category to which many classifications can belong
    """
    name = models.CharField(unique=True, max_length=100)
    help = models.TextField(default=None)

    def save(self, *args, **kwargs):
        """
        Override save method to make only the first letter of the name capital
        """
        val = getattr(self, 'name', False)
        if val:
            setattr(self, 'name', val.lower().capitalize())
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Classification(models.Model):
    """
    A subset of a category to classify recommendations under
    """
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        """
        Override save method to make only the first letter of the name capital
        """
        val = getattr(self, 'name', False)
        if val:
            setattr(self, 'name', val.lower().capitalize())
        super(Classification, self).save(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(str(self.category), self.name)


class Recommendation(models.Model):
    """
    A single recommendation and the classifications to which it belongs. Classifications should be specific enough
    such that it only belongs to one classification per category.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    classification = models.ManyToManyField(Classification)

    def save(self, *args, **kwargs):
        """
        Override save method to make only the first letter of the name capital
        """
        val = getattr(self, 'name', False)
        if val:
            setattr(self, 'name', val.lower().capitalize())
        super(Recommendation, self).save(*args, **kwargs)

    def __str__(self):
        return '{} <-- {}'.format(self.name, '; '.join(str(c) for c in self.classification.all()))


class Contact(models.Model):
    """
    Contact information for an individual
    """
    name = models.CharField(max_length=100, null=True, default=None)
    email = models.EmailField(unique=True)

    def mailto(self, subject=None):
        if subject is None:
            return '<a href="mailto:{}">{}</a>'.format(self.email, self.name)
        else:
            return '<a href="mailto:{}?Subject={}">{}</a>'.format(self.email, quote(subject), self.name)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.email)


class Project(models.Model):
    """
    A collection of recommendations for a specific project
    """
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact = models.ManyToManyField(Contact, blank=True)
    description = models.TextField(default=None)
    trust = models.TextField(default=None)
    item = models.ManyToManyField(Recommendation, blank=True)
    visits = models.PositiveIntegerField(default=0)
    last_visit = models.DateTimeField(default=None, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensure that description and trust are properly cleaned before saving since we allow them to display html
        """
        if self.description:
            self.description = clean(self.description)
        if self.trust:
            self.trust = clean(self.trust)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return 'pk:{} name:{}'.format(self.pid, self.name)

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['item', 'visits', 'last_visit']
        labels = {
            'name' : _('Project Name'),
            'description' : _('Project Description'),
            'trust' : _('Threat Model'),
            'contact' : _('KNOX Security contact')
        }
        help_texts = {
            'name' : _('Enter a brief, preferably unique, name to describe the project'),
            'description' : _('Enter a brief project description summary'),
            'trust' : _('Enter a brief threat model considered for the project'),
            'contact' : _('This/these will be the contact individuals for the review')
        }

# class ProjectEditForm(ModelForm):
#     class Meta:
#         model = Project
