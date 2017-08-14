from django import forms
from django.utils.translation import ugettext_lazy as _
from designsec.models import Category, Classification, Recommendation, Project, Contact


class MakeReadOnlyModelForm(forms.ModelForm):
    def make_readonly(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk is not None:
            for field in self.fields.keys():
                self.fields[field].widget.attrs['disabled'] = True


class CategoryModelForm(MakeReadOnlyModelForm):
    class Meta:
        model = Category
        fields = ['name', 'help']
        help_texts = {
            'name': _('Simple, short category name; no HTML (50 characters max)'),
            'help': _('Slightly longer description of category; no HTML')
        }


class ClassificationModelForm(MakeReadOnlyModelForm):
    class Meta:
        model = Classification
        fields = ['name', 'description', 'category']
        help_texts = {
            'name': _('Brief description of classification within the category; no HTML (100 characters max)'),
            'description': _('Longer description of classification. Should include a broad introduction '
                             'to types of recommendations contained within; some HTML accepted'),
            'category': _('Category to which this is a sub-classification of')
        }


class RecommendationModelForm(MakeReadOnlyModelForm):
    class Meta:
        model = Recommendation
        fields = ['name', 'description', 'classification']
        help_texts = {
            'name': _('Brief description of the recommendation; no HTML (100 characters max)'),
            'description': _('Longer description of the recommendation; some HTML accepted. '
                             'Can include examples, rational, and dangers'),
            'classification': _('Classification(s) to which this recommendation can be categorized')
        }

    def is_valid(self):
        valid = super(RecommendationModelForm, self).is_valid()
        if not valid:
            return valid

        # check to see if we have the 'All' category/classification
        classifications = self.cleaned_data.get('classification')
        if Classification.get_universal_classification_queryset()[0] not in classifications:
            self.cleaned_data['classification'] |= Classification.get_universal_classification_queryset()
        return True


class ContactModelForm(MakeReadOnlyModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email']
        help_texts = {
            'name': _('Name of the contact'),
            'email': _('Email address of contact')
        }


class ProjectModelForm(MakeReadOnlyModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'trust', 'contact']
        labels = {
            'name': _('Project Name'),
            'description': _('Project Description'),
            'trust': _('Threat Model'),
            'contact': _('KNOX Security contact')
        }
        help_texts = {
            'name': _('Enter a brief, preferably unique, name to describe the project'),
            'description': _('Enter a brief project description summary'),
            'trust': _('Enter a brief threat model considered for the project'),
            'contact': _('This/these will be the contact individuals for the review')
        }
