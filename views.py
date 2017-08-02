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
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from designsec.models import Category, Recommendation, Project, Contact, Classification
import designsec.forms as design_forms

# from django.db.models import Q
# from django.forms.models import model_to_dict
knox = Contact.objects.filter(name='Knox Security')[0]

SUPPORTED_MODAL_CLASSES = {
    'project': Project,
    'category': Category,
    'recommendation': Recommendation,
    'contact': Contact,
    'classification': Classification
}
MODAL_MODEL_FORMS = {
    'project': design_forms.ProjectModelForm,
    'category': design_forms.CategoryModelForm,
    'recommendation': design_forms.RecommendationModelForm,
    'contact': design_forms.ContactModelForm,
    'classification': design_forms.ClassificationModelForm
}
MODAL_DELETE_FORMS = {
    'project': design_forms.ProjectDeleteForm,
    'category': design_forms.CategoryDeleteForm,
    'recommendation': design_forms.RecommendationDeleteForm,
    'contact': design_forms.ContactDeleteForm,
    'classification': design_forms.ClassificationDeleteForm
}
# CAUTION: ANY OPTIONS SET HERE WILL OVERRIDE THE OPTIONS FOR ALL OPERATIONS
MODAL_OPTIONS = {
    'project': {
        'select_check': 'contact'
    },
    'recommendation': {
        'select_check': 'classification'
    },
    'classification': {},
    'category': {},
    'contact': {}
}


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
    # if not cat_obj or cat_obj is None:
    #    cat_obj = Category.objects.all()[0]
    # Get the defined classifications for the desired category
    for c in cat_obj.classification_set.order_by('name'):
        rec_dict[c.name] = (c, [])

    # sort the recommendations based on the category classifications
    for l in lst:
        classes = l.classification.filter(category=cat_obj)
        # if the recommendation exists in the desired category, save it with the classification
        for c in classes:
            rec_dict[c.name][1].append((l, Category.objects.filter(classification__recommendation=l).order_by('name')))
    # remove any entries that have no values
    # and convert the rest from a dictionary
    classification_list = []
    popper = []
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
        notice = '<strong>Unable to find the reference locator {}.</strong><br />All '.format(project)
        notice += 'recommendations are displayed. Please contact a member of {} '.format(knox.mailto(subject=subject))
        notice += 'if you believe this is a mistake'
        messages.add_message(request, messages.ERROR, notice)
        return generate_default_view(request)

    context = {'project': p,
               'category': Category.objects.all(),
               'rec_list': get_recommendation_by_category(p_uid=p_uid),
               'pid': project}
    return render(request, 'designsec/main.html', context)


# todo create a helper function similar to get_recommendation_by_category for the default view (?)
#       this might just be done with html

# def get_admin_recommendation_by_category(cat=None, p_uid=None):
#     """
#     Get a list of recommendations based on the desired category for a project
#     :param cat: The id of the recommendation category to sort based on. If none provided, we they will be presented in
#                 the 'All' category.
#     :param p_uid: The project uuid that we are getting the recommendations from. If none provided, we will get
#                   all recommendations.
#     :return
#     """
#     pass


# todo ensure that user is properly authenticated before edits happen!

def create_new_project(request):
    """
    ADMIN INTERFACE

    When a project is created, the necessary info needs to be provided. This information is defined in
    models.ProjectModelForm. If any fields do not pass validation, a JSON object will be returned with all of the error
    messages. Upon successful project creation, the HTML document for a new list admin interface will be returned.

    If you try to access this interface without a POST request, you will be redirected to the admin list interface.

    :param request: HTTP request object containing request metadata
    :return: JSON object if unsuccessful, HTML document if successful
    """
    # todo do we want to change this to have a uniform functionality? We can return HTML for everything. If something
    #       is invalid, it can be rendered as such in the next display. We can also keep put the current info into the
    #       form https://docs.djangoproject.com/en/1.11/ref/forms/api/#how-errors-are-displayed
    # todo we might want to convert to a modelformset_factory from our custom formset. This will allow us to specify
    #       specific formsets on the fly. We can also achieve by creating more custom formsets (i.e. selecting
    #       recommendations)
    if request.method == "POST":
        formset = design_forms.ProjectModelForm(request.POST)
        if formset.is_valid():
            p = formset.save()
            messages.add_message(request, messages.SUCCESS, 'Project created with id {}'.format(p.pid.hex))
            return redirect('list')

        else:
            response = JsonResponse(formset.errors.as_json(), safe=False)
            response.status_code = 400
            return response
    return redirect('list')


def delete_project(request):
    """
    ADMIN INTERFACE

    This function can be used to delete a project. The functionality can only be accessed by a POST request. If there
    is no POST, it will return a 405 error code. Successful POST responses will also send a redirected 'list' page. It
    is up to the receiving AJAX call to strip the body to update its current page.

    :param request: HTTP request object containing request data
    :return: A rendered HTML document of the admin list page or 405 error. A message will be included at the top if
             necessary
    """
    if request.method == "POST":
        pid = request.POST.get('project', None)
        if pid is not None:
            p_uid = uuid.UUID(pid)
            p = Project.objects.filter(pid=p_uid)
            if p:
                if len(p) != 1:
                    messages.add_message(request, messages.ERROR, 'Project id {} is not unique. You will '
                                                                  'have to delete it manually.'.format(pid))
                else:
                    p.delete()
                    messages.add_message(request, messages.SUCCESS, 'Project with id {} successfully '
                                                                    'deleted'.format(pid))
        else:
            messages.add_message(request, messages.ERROR, 'No project id provided to delete.')
        return redirect('list')
    return HttpResponseNotAllowed(permitted_methods=['POST'])


def get_modal(request, op=None):
    """
    ADMIN INTERFACE

    This is the master method used to get the desired modal.
    :param request:
    :param op: Type of modal to get (add, edit, delete)
    :return:
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    if request.POST.get('target', None) not in SUPPORTED_MODAL_CLASSES:
        return HttpResponseBadRequest()
    # Determine what class we are trying to make a modal for
    target = request.POST.get('target')
    # Some operations do not need an ID
    if op == 'add':
        return add_modal(request, target)
    # The rest need an ID
    t_id = request.POST.get('id', None)
    try:
        target_obj = get_object_or_404(SUPPORTED_MODAL_CLASSES, pk=t_id)
    except Http404:
        response = JsonResponse({'status': '400', 'reason': 'Invalid ID provided'})
        response.status_code = 400
        return response
    if op == 'add':
        return edit_modal(request, target, target_obj)
    elif op == 'delete':
        return delete_modal(request, target, target_obj)


# todo use jquery to get the object we are acting on and the field name for any multi-select.
#       Generate add button dynamically?

# todo when creating a recommendation, make sure that only one classification of each category exists
#   if more than one category, present an error to be more specific and tailor it to one classification.

def add_modal(request, target):
    formset = MODAL_MODEL_FORMS[target]
    if request.POST.get('loaded', None) is not None:
        # we have already been here once, validate and try to save the form
        loaded = formset(request.POST_)
        if loaded.is_valid():
            # todo when adding a recommendation, make sure to add it to the 'All' category!
            p = loaded.save()
            # todo we probably just want to return a json message
            messages.add_message(request, messages.SUCCESS, '{} created with id {}'.format(target.capitalize(),
                                                                                           p.pid.hex))
            return redirect('list')

        else:
            response = JsonResponse(loaded.errors.as_json(), safe=False)
            response.status_code = 400
            return response
    # generate the form for the first time
    context = {
        'operation': 'add',
        'target': target,
        'formset': formset(),
        'select_check': '',
        'success_color': 'success',
        'cancel_color': 'danger'
    }
    context.update(MODAL_OPTIONS[target])
    # todo complete this JsonResponse object, propagate to other modals/results
    response = JsonResponse({
        'form_id': '',
        'next_action': '',
        'modal': render_to_string('designsec/admin_modal_form.html', context, request)
    })
    response.status_code = 200
    return response


# todo we need to be able to specify the action for jquery to perform when modal is closed.

def edit_modal(request, target, edit_target):
    # Determine what formset we are trying to show
    formset = MODAL_MODEL_FORMS[target]
    if request.POST.get('loaded', None) is not None:
        # we have already been here once, validate and try to save the form
        loaded = formset(request.POST)
        if loaded.is_valid():
            loaded.save()
            return HttpResponse(status=200)
        response = JsonResponse(loaded.errors.as_json(), safe=False)
        response.status_code = 400
        return response
    # generate the form for the first time
    context = {
        'operation': 'edit',
        'target': target,
        'formset': formset(instance=edit_target),
        'select_check': '',
        'success_color': 'success',
        'cancel_color': 'danger'
    }
    context.update(MODAL_OPTIONS[target])
    return render(request, 'designsec/admin_modal_form.html', context)


def delete_modal(request, target, edit_target):
    form = MODAL_DELETE_FORMS[target]
    if request.POST.get('loaded', None) is not None:
        # we have already been here once, validate and try to delete the object
        loaded = form(request.POST)
        if loaded.is_valid():
            edit_target.delete()
            return HttpResponse(status=200)
        response = JsonResponse(loaded.errors.as_json(), safe=False)
        response.status_code = 400
        return response
    # generate the form for the first time
    context = {
        'operation': 'delete',
        'target': target,
        'formset': form(edit_target),
        'select_check': '',
        'success_color': 'success',
        'cancel_color': 'danger'
    }
    context.update(MODAL_OPTIONS[target])


def generate_edit_project_view(request, project):
    """
    ADMIN INTERFACE

    :param request: HTTP request object containing request metadata
    :param project:
    :return:
    """
    # todo complete this, change from main.html
    # todo when modifying a project, make sure that changes are applied before switching categories
    #       keep when switching categories, submit list of selected and non-selected recommendations displayed
    # todo for each category, make a modal to create a new recommendation
    #       create modals with JS by passing category/classification that we belong to
    #       when a recommendation is successfully created, save the current selection in JS and apply on new list load
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
    """
    ADMIN INTERFACE

    List all projects along with their permalinks, creation date, number of recommendations, updated date, number of
    views, and last visit
    :param request: HTTP request object containing request metadata
    :return:
    """
    # todo provide an interface to edit/add contacts, make available as a modal from admin list
    context = {'projects': []}
    for p in Project.objects.all():
        pr = {
            'name': p.name,
            'pid_short': '{}...'.format(p.pid.hex[:8]),
            'pid': p.pid.hex,
            'added': p.added,
            'modified': p.modified,
            'contact': '; '.join([c.email.split('@')[0] for c in p.contact.order_by('email')]),
            'rec_count': p.item.count(),
            'last_visit': p.last_visit
        }
        context['projects'].append(pr)

    modal = {
        'operation': 'create',
        'target': 'project',
        'formset': design_forms.ProjectModelForm(),
        'select_check': 'contact',
        'success_color': 'success',
        'cancel_color': 'danger'
    }

    context['modal'] = render_to_string('designsec/admin_modal_form.html', modal, request)

    return render(request, 'designsec/adminList.html', context)
