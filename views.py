# Generate the HTML content by sorting for a specific category
# Generate a response wrapping the previous

# Generate a view for the admin where you can add items
#   for each item, break on newline and add a <p></p> around each paragraph
#   strip out each html tag that is not supported.
#       This will also have to allow the admin to create new classifications
#           Specify classications for each category
#       Each time a tag is added, make sure to add it to a default classification for each category
# Allow the admin to create a new category
# Allow the admin to create new classifications
# Allow the admin to drag the recommendations around to different classifications

# When adding a new item, create a popup to specify the classification for each category?


# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse, HttpResponse, Http404
# from django.db.models import Q
# from django.forms.models import model_to_dict

from .models import Category, Recommendation, SecurityList


def get_recommendation_by_category(cat=None, project=None):
    """
    Get a sorted list of recommendations
    :param cat: The recommendation category to sort based on. If none provided, we they will be sorted based on the
                first category in the database.
    :param project: The project that we are getting the recommendations from. If none provided, we will get all
                    all recommendations.
    :return: A dictionary of recommendations keyed on the category classification
    """
    # todo convert the dictionary to a form that can preserve classification order
    # todo rename s_list to have an accurate name
    if project is None:
        lst = Recommendation.objects.all()
    else:
        lst = SecurityList.objects.filter(pk=project).values('item').distinct()

    s_list = dict()
    cat_obj = Category.objects.filter(name=cat)
    # If we do not have a valid category, just get the first one defined.
    if not cat_obj or cat_obj is None:
        cat_obj = Category.objects.limit(1)
    # Get the defined classifications for the desired category
    for c in cat_obj.classification_set.order_by('name'):
        s_list[c.name] = []

    # sort based on the category. If items have no classification for the category, put them in 'Not Classified'
    s_list['Not Classified'] = []
    for l in lst:
        if l.classification.name is not None:
            s_list[l.classification.name].append(l)
        else:
            s_list['Not Classified'].append(l)
    # remove any entries that have no values
    for k, v in s_list.items():
        if not v:
            s_list.pop(k)

    return s_list


def generate_default_view(request):
    """
    Generate the view that includes all recommendations without a project description.
    :param request:
    :return:
    """
    pass


def generate_recommendation_by_category(request, project):
    """

    :param request:
    :param project:
    :return:
    """
    pass


def generate_project_view(request, project):
    """

    :param request:
    :param project:
    :return:
    """
    # todo keep track of the number of views and the last view as long as an admin is not logged in (maybe?)
    pass

# todo create a helper function similar to get_recommendation_by_category for the default view (?) -- this might just be done with html

# todo create a function & url to save a category/classification/recommendation (and how this will be displayed) -- use a modal?

def create_new_project(request):
    """
    ADMIN INTERFACE

    :param request:
    :return:
    """
    pass


def edit_project(request, project):
    """
    ADMIN INTERFACE

    :param request:
    :param project:
    :return:
    """
    pass


def list_projects(request):
    '''
    ADMIN INTERFACE

    List all projects along with their permalinks, creation date, updated date, number of views, and last visit
    :param request:
    :return:
    '''
    # todo allow this view to sort the projects in ascending/descending according to each field
    pass
