from django import forms
from django.utils.translation import ugettext_lazy as _
from designsec.models import Category, Classification, Recommendation, Project, Contact


class MakeReadOnlyModelForm(forms.ModelForm):

    def make_readonly(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields.keys():
                self.fields[field].widget.attrs['readonly'] = True


class CategoryModelForm(MakeReadOnlyModelForm):
    class Meta:
        model = Category
        fields = ['name', 'help']
        help_texts = {
            'name': _('Simple, short category name; no HTML (50 characters max)'),
            'help': _('Slightly longer description of category; no HTML')
        }

    def is_valid(self):
        valid = super(CategoryModelForm, self).is_valid()
        if not valid:
            return valid

        # Check to make sure that we are not the 'All' category
        if self.cleaned_data['name'] == 'All' and self.cleaned_data.get('DELETE', False):
            self.add_error('name', {'message': 'You cannot delete the \'All\' category.'})
            return False
        return True


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

    def is_valid(self):
        valid = super(ClassificationModelForm, self).is_valid()
        if not valid:
            return valid

        # Check to make sure that we are not deleting the last 'All' classification
        if Category.objects.filter(name='All').count() == 1 and \
                Classification.objects.filter(id=self.cleaned_data['id'])[0].category.name == 'All' and \
                self.cleaned_data['category'].name == 'All' and \
                self.cleaned_data.get('DELETE', False):
            self.add_error('category', {'message': 'This change will remove the last classification from the '
                                                   '\'All\' category. This operation is forbidden.'})
            return False
        return True


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
