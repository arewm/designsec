import uuid
from urllib.parse import quote
from django.db import models
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

# Add to the beach.clean whitelist settings. Customized based on tags inserted by tinymce editor
ALLOWED_TAGS.extend(['p', 'sup', 'sub', 'div', 'br', 'span',
                     'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                     'table', 'tbody', 'thead', 'tr', 'td', 'th'])
ALLOWED_ATTRIBUTES.update({
    'p': ['style'],
    'span': ['style'],
    'table': ['style', 'cellpadding', 'cellspacing', 'border'],
    'th': ['style'],
    'td': ['style']
})
ALLOWED_ATTRIBUTES['a'].extend(['target', 'rel'])
ALLOWED_STYLES.extend(['padding-left', 'text-decoration', 'text-align', 'vertical-align'
                       'width', 'height', 'margin-left', 'margin-right'])


class Category(models.Model):
    """
    A category to which many classifications can belong

    ..note: There should always be an 'All' Category. We have ensured this using the CategoryModelForm, but be careful
            if playing around with the objects directly!
    """
    name = models.CharField(unique=True, max_length=50)
    help = models.CharField(default=None, max_length=100)

    def save(self, *args, **kwargs):
        """
        Override save method to make only the first letter of the name capital
        """
        if self.name:
            self.name = self.name.lower().capitalize()
        super(Category, self).save(*args, **kwargs)

    def can_delete(self):
        """
        Determine whether the current model can be deleted

        :return: boolean; reason why we cannot delete
        """
        if self.name == 'All':
            return False, ('name', 'You cannot delete the \'All\' category.')
        return True, ''

    def delete(self, *args, **kwargs):
        """
        Override to only delete if the object is deletable

        :param args:
        :param kwargs:
        :return:
        """
        deletable, _ = self.can_delete()
        if deletable:
            return super(Category, self).delete(*args, **kwargs)

    @staticmethod
    def get_universal_category():
        return Category.objects.filter(name='All')[0]

    def __str__(self):
        return '{}'.format(self.name)


class Classification(models.Model):
    """
    A subset of a category to classify recommendations under

    ..note: There should always be a classification that belongs to an 'All' Category. We have ensured this using the
            ClassificationModelForm, but be careful if playing around with the objects directly!
    """
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('name', 'category')

    def save(self, *args, **kwargs):
        """
        Override save method to make only the first letter of the name capital; ensure that html is properly cleaned
        """
        if self.name:
            self.name = self.name.lower().capitalize()
        if self.description:
            self.description = clean(self.description)
        # make sure that there is only ever one classification within the 'All' category
        all_category = Category.get_universal_category()
        if self.category == all_category:
            if self.name == 'All':
                super(Classification, self).save(*args, **kwargs)
        else:
            super(Classification, self).save(*args, **kwargs)

    def can_delete(self):
        """
        Determine whether the current model can be deleted

        :return: boolean; reason why we cannot delete
        """
        # self.cleaned_data.get('DELETE', False) and Category.objects.filter(name='Test').count() == 1 and \
        # Classification.objects.filter(pk=self.cleaned_data['pk'])[0].category.name == 'Test' and \
        # self.cleaned_data['category'].name == 'Test':
        if Category.objects.filter(name='All').count() == 1 and \
                Classification.objects.filter(pk=self.pk)[0].category.name == 'All':
            return False, ('name', 'This change will remove the last classification from the \'All\' category. This '
                                   'operation is forbidden.')
        return True, ''

    def delete(self, *args, **kwargs):
        """
        Override to only delete if the object is deletable

        :param args:
        :param kwargs:
        :return:
        """
        deletable, _ = self.can_delete()
        if deletable:
            return super(Classification, self).delete(*args, **kwargs)

    @staticmethod
    def get_universal_classification_queryset():
        return Classification.objects.filter(category=Category.get_universal_category())

    def __str__(self):
        return '{}: {}'.format(str(self.category), self.name)


class Recommendation(models.Model):
    """
    A single recommendation and the classifications to which it belongs. Classifications should be specific enough
    such that it only belongs to one classification per category.

    ..note: The 'ALL' classification/category should always be added. We have ensured this using
            RecommendationModelForm, but be careful if playing around with the objects directly!
    """
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    classification = models.ManyToManyField(Classification)

    def save(self, *args, **kwargs):
        """
        Override save method to make only the first letter of the name capital; Ensure that html is properly cleaned
        """
        if self.name:
            self.name = self.name.lower().capitalize()
        if self.description:
            self.description = clean(self.description)
        super(Recommendation, self).save(*args, **kwargs)

    def can_delete(self):
        """
        Determine whether the current model can be deleted

        :return: boolean; reason why we cannot delete
        """
        return True, ''

    def delete(self, *args, **kwargs):
        """
        Override to only delete if the object is deletable

        :param args:
        :param kwargs:
        :return:
        """
        deletable, _ = self.can_delete()
        if deletable:
            return super(Recommendation, self).delete(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


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

    def can_delete(self):
        """
        Determine whether the current model can be deleted

        :return: boolean; reason why we cannot delete
        """
        return True, ''

    def delete(self, *args, **kwargs):
        """
        Override to only delete if the object is deletable

        :param args:
        :param kwargs:
        :return:
        """
        deletable, _ = self.can_delete()
        if deletable:
            return super(Contact, self).delete(*args, **kwargs)

    def __str__(self):
        return '{} <{}>'.format(self.name, self.email)


class Project(models.Model):
    """
    A collection of recommendations for a specific project
    """
    pid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    contact = models.ManyToManyField(Contact, blank=True)
    description = models.TextField(default=None)
    trust = models.TextField(default=None)
    recommendation = models.ManyToManyField(Recommendation, blank=True)
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

    def can_delete(self):
        """
        Determine whether the current model can be deleted

        :return: boolean; reason why we cannot delete
        """
        return True, ''

    def delete(self, *args, **kwargs):
        """
        Override to only delete if the object is deletable

        :param args:
        :param kwargs:
        :return:
        """
        deletable, _ = self.can_delete()
        if deletable:
            return super(Project, self).delete(*args, **kwargs)

    def __str__(self):
        return 'pid:{} name:{}'.format(self.pid, self.name)
