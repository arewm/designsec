# Generate the HTML content by sorting for a specific category
# Generate a response wrapping the previous

# Generate a view for the admin where you can add items
#   for each item, break on newline and add a <p></p> around each paragraph
#   strip out each html tag that is not supported.
#       This will also have to allow the admin to create new classifications
#           Specify classifications for each category
#       Each time a tag is added, make sure to add it to a default classification for each category
# Allow the admin to create a new category
# Allow the admin to create new classifications
# Allow the admin to drag the recommendations around to different classifications

# When adding a new item, create a popup to specify the classification for each category?

import uuid

from django.http import Http404
from django.shortcuts import render, get_object_or_404

from designsec.models import Category, Recommendation, Project


# from django.db.models import Q
# from django.forms.models import model_to_dict


def get_recommendation_by_category(cat=None, p_uid=None):
    """
    Get a list of recommendations based on the desired category for a project
    :param cat: The id of the recommendation category to sort based on. If none provided, we they will be presented in
                the 'All' category.
    :param p_uid: The project uuid that we are getting the recommendations from. If none provided, we will get
                  all recommendations.
    :return: A list of classification, recommendation list tuples
    """
    try:
        p = get_object_or_404(Project, pid=p_uid)
        lst = p.item.all()
    except Http404:
        lst = Recommendation.objects.all()

    rec_dict = dict()
    try:
        cat_obj = get_object_or_404(Category, id=cat)
    except Http404:
        # If we do not have a valid category, just get the first one defined.
        cat_obj = get_object_or_404(Category, name='All')
    # If we do not have a valid category, just get the first one defined.
    #if not cat_obj or cat_obj is None:
    #    cat_obj = Category.objects.all()[0]
    # Get the defined classifications for the desired category
    for c in cat_obj.classification_set.order_by('name'):
        rec_dict[c.name] = []

    # sort the recommendations based on the category classifications
    not_classified = []
    for l in lst:
        classes = l.classification.filter(category=cat_obj)
        # if the recommendation does not match our category, it is not classified
        if not classes:
            not_classified.append(l)
        # otherwise, put it in the proper dictionary place
        else:
            for c in classes:
                rec_dict[c.name].append(l)
    # remove any entries that have no values
    # and convert the rest from a dictionary
    classification_list = []
    popper=[]
    for k, v in rec_dict.items():
        if not v:
            popper.append(k)
        else:
            classification_list.append((k, v))
    for p in popper:
        rec_dict.pop(p)

    # sort the list based on the classification and put any non-classified recommendations at the end
    classification_list.sort(key=lambda x: x[0])
    if not_classified:
        classification_list.append(('Not classified', not_classified))

    return classification_list


def generate_default_view(request, notice=None):
    """
    Generate the view that includes all recommendations without a project description.
    :param request: HTTP request object containing request metadata
    :param notice: A notice to display at the top of the rendered page
    :return:
    """
    if notice is None:
        notice = 'Since no project was selected, all possible recommendations are displayed. '
        notice += 'To customize the recommendations for  your project, contact a member of '
        notice += '<a href="mailto:knox_security@samsung.com?Subject=Security%20recommendation%20request">'
        notice += 'Knox Security</a> to begin a security review.'

    context = {'notice': notice,
               'description': '',
               'trust': '',
               'category': Category.objects.all(),
               'rec_list': get_recommendation_by_category()}
    return render(request, 'designsec/main.html', context)


def generate_recommendation_by_category(request, project=None):
    """
    Sort the recommendations for a project based on the passed POST parameters
    :param request: HTTP request object containing request metadata
    :param project: The pid that we are looking up (as a hex)
    :return: The rendered webpage
    """
    # todo complete this
    context = {'rec_list': get_recommendation_by_category(cat=request.POST.get('category', None), p_uid=project)}
    return render(request, 'designsec/main-recommendations.html', context)


def generate_project_view(request, project):
    """
    Generate the default view for a specified project. If the project cannot be found, a default view will be generated
    :param request: HTTP request object containing request metadata
    :param project: The project to display the information for
    :return: The rendered webpage
    """
    # todo keep track of the number of views and the last view as long as an admin is not logged in (maybe?)
    # todo allow a specific sorting to be permalinked

    p_uid = uuid.UUID(project)
    try:
        p = get_object_or_404(Project, pid=p_uid)
    except Http404:
        notice = '<strong>Unable to find the reference locator {}.</strong><br />All recommendations are displayed. '.format(project)
        notice += 'Please contact a member of <a href="mailto:knox_security@samsung.com'
        notice += '?Subject=Security%20recommendation%20bad%20pid{}">'.format(project)
        notice += 'Knox Security</a> if you believe this is a mistake.'
        return generate_default_view(request, notice=notice)

    context = {'notice': False,
               'project': p,
               'category': Category.objects.all(),
               'rec_list': get_recommendation_by_category(p_uid=p_uid),
               'pid': project}
    return render(request, 'designsec/main.html', context)


# todo create a helper function similar to get_recommendation_by_category for the default view (?) -- this might just be done with html

# todo create a function & url to save a category/classification/recommendation (and how this will be displayed) -- use a modal?

# todo when adding a recommendation/classification, make sure to add it to the 'All' category!

def create_new_project(request):
    """
    ADMIN INTERFACE

    :param request: HTTP request object containing request metadata
    :return:
    """
    pass


def edit_project(request, project):
    """
    ADMIN INTERFACE

    :param request: HTTP request object containing request metadata
    :param project:
    :return:
    """
    pass


def list_projects(request):
    '''
    ADMIN INTERFACE

    List all projects along with their permalinks, creation date, updated date, number of views, and last visit
    :param request: HTTP request object containing request metadata
    :return:
    '''
    # todo allow this view to sort the projects in ascending/descending according to each field
    pass
