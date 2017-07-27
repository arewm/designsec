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

from django.contrib import messages
from django.forms import modelformset_factory
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.safestring import mark_safe

from designsec.models import Category, Recommendation, Project, Contact, ProjectForm

# from django.db.models import Q
# from django.forms.models import model_to_dict
knox = Contact.objects.filter(name='Knox Security')[0]


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
        rec_dict[c.name] = (c,[])

    # sort the recommendations based on the category classifications
    for l in lst:
        classes = l.classification.filter(category=cat_obj)
        # if the recommendation exists in the desired category, save it with the classification
        for c in classes:
            rec_dict[c.name][1].append((l, Category.objects.filter(classification__recommendation=l).order_by('name')))
    # remove any entries that have no values
    # and convert the rest from a dictionary
    classification_list = []
    popper=[]
    for k, v in rec_dict.items():
        if not v[1]:
            popper.append(k)
        else:
            classification_list.append((k, v[0], v[1]))
    for p in popper:
        rec_dict.pop(p)

    # sort the list based on the classification and the recommendation
    classification_list.sort(key=lambda x: x[0])
    # sort the recommendations for each classification
    [r[2].sort(key=lambda x: x[0].name) for r in classification_list]

    return classification_list


def generate_default_view(request):
    """
    Generate the view that includes all recommendations without a project description.
    :param request: HTTP request object containing request metadata
    :return:
    """
    if not messages.get_messages(request):
        notice = 'No project was selected. All possible recommendations are displayed. '
        notice += 'To customize the recommendations for  your project, contact a member of '
        notice += '{} to begin a security review.'.format(knox.mailto('Security recommendation request'))
        messages.add_message(request, messages.WARNING, notice)

    context = {'description': '',
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
        subject = 'Security recommendation bad project id {}'.format(project)
        notice = '<strong>Unable to find the reference locator {}.</strong><br />All recommendations are displayed. '.format(project)
        notice += 'Please contact a member of {} if you believe this is a mistake'.format(knox.mailto(subject=subject))
        messages.add_message(request, messages.ERROR, notice)
        return generate_default_view(request)

    context = {'project': p,
               'category': Category.objects.all(),
               'rec_list': get_recommendation_by_category(p_uid=p_uid),
               'pid': project}
    return render(request, 'designsec/main.html', context)


# todo create a helper function similar to get_recommendation_by_category for the default view (?) -- this might just be done with html

# todo create a function & url to save a category/classification/recommendation (and how this will be displayed) -- use a modal?

# todo when adding a recommendation/classification, make sure to add it to the 'All' category!
# todo when creating a recommendation, make sure that only one classification of each category exists
#   if more than one category, present an error to be more specific and tailor it to one classification.

def get_admin_recommendation_by_category(cat=None, p_uid=None):
    """
    Get a list of recommendations based on the desired category for a project
    :param cat: The id of the recommendation category to sort based on. If none provided, we they will be presented in
                the 'All' category.
    :param p_uid: The project uuid that we are getting the recommendations from. If none provided, we will get
                  all recommendations.
    :return
    """
    pass

def create_new_project(request):
    """
    ADMIN INTERFACE

    When a project is created, the necessary info needs to be provided. This information is defined in
    models.ProjectForm. If any fields do not pass validation, a JSON object will be returned with all of the error
    messages. Upon successful project creation, the HTML document for a new list admin interface will be returned.

    If you try to access this interface without a POST request, you will be redirected to the admin list interface.

    :param request: HTTP request object containing request metadata
    :return: JSON object if unsuccessful, HTML document if successful
    """
    if request.method == "POST":
        formset = ProjectForm(request.POST)
        if formset.is_valid():
            p = formset.save()
            messages.add_message(request, messages.SUCCESS, 'Project created with id {}'.format(p.pid.hex))
            return redirect('list')

        else:
            return JsonResponse(formset.errors.as_json(), safe=False)
    return redirect('list')


def edit_project(request, project):
    """
    ADMIN INTERFACE

    :param request: HTTP request object containing request metadata
    :param project:
    :return:
    """
    # todo complete this, change from main.html
    # todo when modifying a project, make sure that changes are applied before switching categories
    # todo for each category, make a modal to create a new recommendation
        # todo how do you handle when a recommendation is added and selections have been made?
    p_uid = uuid.UUID(project)
    try:
        p = get_object_or_404(Project, pid=p_uid)
    except Http404:
        # This is not a valid project ID to edit, default to list_project
        messages.add_message(request, messages.WARNING, "The project ID {} is invalid.".format(project))
        return redirect('list')

    context = {'project': p,
               'category': Category.objects.all(),
               'rec_list': get_recommendation_by_category(p_uid=p_uid),
               'pid': project}
    return render(request, 'designsec/main.html', context)


def list_projects(request):
    '''
    ADMIN INTERFACE

    List all projects along with their permalinks, creation date, number of recommendations, updated date, number of
    views, and last visit
    :param request: HTTP request object containing request metadata
    :return:
    '''
    # todo provide an interface to edit/add contacts, make available as a modal from admin list
    context = {'projects':[]}
    for p in Project.objects.all():
        pr = {}
        pr['name'] = p.name
        pr['pid_short'] = '{}...'.format(p.pid.hex[:8])
        pr['pid'] = p.pid.hex
        pr['added'] = p.added
        pr['modified'] = p.modified
        pr['contact'] = '; '.join([c.email.split('@')[0] for c in p.contact.order_by('email')])
        pr['rec_count'] = p.item.count()
        pr['last_visit'] = p.last_visit
        context['projects'].append(pr)

    #ProjectFormSet = modelformset_factory(Project, exclude=['item', 'visits', 'last_visit'])
    context['contact_formset'] = ProjectForm()

    return render(request, 'designsec/adminList.html', context)
