from django import forms
from django.utils.translation import ugettext_lazy as _
from designsec.models import Category, Classification, Recommendation, Project, Contact


class NoDeleteModelForm(forms.ModelForm):
    def is_valid(self):
        if not super(NoDeleteModelForm, self).is_valid():
            return False

        if self.cleaned_data['DELETE']:
            self.add_error(None, {'message': 'You cannot use this form to delete %(model_name)s.'})
            return False
        return True


class CategoryModelForm(NoDeleteModelForm):
    class Meta:
        model = Category
        fields = ['name', 'help']
        help_texts = {
            'name': _('Simple, short category name; no HTML (50 characters max)'),
            'help': _('Slightly longer description of category; no HTML')
        }


class CategoryDeleteForm(forms.Form):
    name = forms.CharField(disabled=True)
    help = forms.CharField(disabled=True)

    def __init__(self, category, *args, **kwargs):
        kwargs['initial'] = {
            'name': category.name,
            'help': category.help
        }
        super(CategoryDeleteForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(CategoryDeleteForm, self).is_valid()
        if not valid:
            return valid

        # Check to make sure that we are not the 'All' category
        if self.cleaned_data['name'] == 'All' and self.cleaned_data['DELETE']:
            self.add_error('name', {'message': 'You cannot delete the \'All\' category.'})
            return False
        return True


class ClassificationModelForm(NoDeleteModelForm):
    class Meta:
        model = Classification
        fields = ['name', 'description', 'category']
        help_texts = {
            'name': _('Brief description of classification within the category; no HTML (100 characters max)'),
            'description': _('Longer description of classification. Should include a broad introduction '
                             'to types of recommendations contained within; some HTML accepted'),
            'category': _('Category to which this is a sub-classification of')
        }


class ClassificationDeleteForm(forms.Form):
    name = forms.CharField(disabled=True)
    description = forms.CharField(disabled=True, max_length=200)
    category = forms.CharField(disabled=True)

    def __init__(self, classification, *args, **kwargs):
        kwargs['initial'] = {
            'name': classification.name,
            'description': classification.description,
            'category': classification.category
        }
        super(ClassificationDeleteForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(ClassificationDeleteForm, self).is_valid()
        if not valid:
            return valid

        # Check to make sure that we are not deleting the last 'All' classification
        if Category.objects.filter(name='All').count() == 1 and \
            Classification.objects.filter(id=self.cleaned_data['id'])[0].category.name == 'All' and \
            self.cleaned_data['category'].name == 'All' and \
            self.cleaned_data['DELETE']:
            self.add_error('category', {'message': 'This change will remove the last classification from the \'All\''
                                                   'category. This operation is forbidden.'})
            return False
        return True


class RecommendationModelForm(NoDeleteModelForm):
    class Meta:
        model = Recommendation
        fields = ['name', 'description', 'classification']
        help_texts = {
            'name': _('Brief description of the recommendation; no HTML (100 characters max)'),
            'description': _('Longer description of the recommendation; some HTML accepted. '
                             'Can include examples, rational, and dangers'),
            'classification': _('Classification(s) to which this recommendation can be categorized')
        }


class RecommendationDeleteForm(forms.Form):
    name = forms.CharField(disabled=True)
    description = forms.CharField(disabled=True, max_length=200)
    classification = forms.CharField(disabled=True)

    def __init__(self, recommendation, *args, **kwargs):
        kwargs['initial'] = {
            'name': recommendation.name,
            'description': recommendation.description,
            'classification': recommendation.classification
        }
        super(RecommendationDeleteForm, self).__init__(*args, **kwargs)


class ContactModelForm(NoDeleteModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email']
        help_texts = {
            'name': _('Name of the contact'),
            'email': _('Email address of contact')
        }


class ContactDeleteForm(forms.Form):
    name = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)

    def __init__(self, contact, *args, **kwargs):
        kwargs['initial'] = {
            'name': contact.name,
            'email': contact.email
        }
        super(ContactDeleteForm, self).__init__(*args, **kwargs)


class ProjectModelForm(NoDeleteModelForm):
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


class ProjectDeleteForm(forms.Form):
    name = forms.CharField(disabled=True)
    description = forms.CharField(disabled=True, max_length=200)
    trust = forms.CharField(disabled=True, max_length=200)
    contact = forms.CharField(disabled=True)

    def __init__(self, project, *args, **kwargs):
        kwargs['initial'] = {
            'name': project.name,
            'description': project.description,
            'trust': project.trust,
            'contact': project.contact
        }
        super(ProjectDeleteForm, self).__init__(*args, **kwargs)
