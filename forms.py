from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from designsec.models import Category, Classification, Recommendation, Project, Contact


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        help_texts = {
            'name' : _('Simple, short category name; no HTML (50 characters max)'),
            'help' : _('Slightly longer description of category; no HTML')
        }

class ClassificationForm(ModelForm):
    class Meta:
        model = Classification
        fields = '__all__'
        help_texts = {
            'name' : _('Brief description of classification within the category; no HTML (100 characters max)'),
            'description' : _('Longer description of classification. Should include a broad introduction '
                              'to types of recommendations contained within; some HTML accepted'),
            'category' : _('Category to which this is a sub-classification of')
        }

class RecommendationForm(ModelForm):
    class Meta:
        model = Recommendation
        fields = '__all__'
        help_texts = {
            'name' : _('Brief description of the recommendation; no HTML (100 characters max)'),
            'description' : _('Longer description of the recommendation; some HTML accepted. '
                              'Can include examples, rational, and dangers'),
            'classification' : _('Classification(s) to which this recommendation can be categorized')
        }

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        help_texts = {
            'name' : _('Simple name of the contact'),
            'email' : _('Email address of contact')
        }

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