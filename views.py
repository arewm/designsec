# Generate the HTML content by sorting for a specific category
# Generate a response wrapping the previous

# Generate a view for the admin where you can add items
#   for each recommendation, break on newline and add a <p></p> around each paragraph
#   strip out each html tag that is not supported.
#       This will also have to allow the admin to create new classifications
#           Specify classifications for each category
#       Each time a tag is added, make sure to add it to a default classification for each category
# Allow the admin to create a new category
# Allow the admin to create new classifications
# Allow the admin to drag the recommendations around to different classifications

# When adding a new recommendation, create a popup to specify the classification for each category?

import uuid

from django.contrib import messages
from django.http import Http404, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from designsec.models import Category, Recommendation, Project, Contact, Classification
from designsec.forms import ProjectModelForm, CategoryModelForm, \
    RecommendationModelForm, ContactModelForm, ClassificationModelForm

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
    'project': ProjectModelForm,
    'category': CategoryModelForm,
    'recommendation': RecommendationModelForm,
    'contact': ContactModelForm,
    'classification': ClassificationModelForm
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


def redirect_to_default_view(request):
    return redirect('default', permanent=True)


def get_recommendation_by_category(cat=None, p_uid=None):
    """
    Get a list of recommendations based on the desired category for a project
    :param cat: The id of the recommendation category to sort based on. If none provided, we they will be presented in
                the 'All' category.
    :param p_uid: The project uuid that we are getting the recommendations from. If none provided, we will get
                  all recommendations.
    :return: A list of classification, recommendation list tuples
    """
    uid=None
    if p_uid is not None:
        uid = uuid.UUID(p_uid)
    try:
        p = get_object_or_404(Project, pid=uid)
        lst = p.recommendation.all()
    except Http404:
        lst = Recommendation.objects.all()

    rec_dict = dict()
    try:
        cat_obj = get_object_or_404(Category, id=cat)
    except Http404:
        # If we do not have a valid category, just get the first one defined.
        cat_obj = get_object_or_404(Category, name='All')

    # Get the defined classifications for the desired category
    for c in cat_obj.classification_set.order_by('name'):
        rec_dict[c.name] = (c, [])

    # sort the recommendations based on the category classifications
    for l in lst:
        classes = l.classification.filter(category=cat_obj)
        # if the recommendation exists in the desired category, save it with the classification
        for c in classes:
            rec_dict[c.name][1].append((l, Category.objects.filter(classification__recommendation=l).order_by('name')))
    # remove any classifications that have no recommendations
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

    return classification_list, cat_obj


def generate_default_view(request, category=None):
    """
    Generate the view that includes all recommendations without a project description.
    :param request: HTTP request object containing request metadata
    :return:
    """
    if category is None:
        category = request.GET.get('category', None)
    if not messages.get_messages(request):
        notice = 'No project was selected. All possible recommendations are displayed. '
        notice += 'To customize the recommendations for  your project, contact a member of '
        notice += '{} to begin a security review.'.format(knox.mailto('Security recommendation request'))
        messages.add_message(request, messages.WARNING, notice)

    recommendations, cat_obj = get_recommendation_by_category()
    context = {
        'description': '',
        'trust': '',
        'category': Category.objects.all(),
        'category_request': category,
        'rec_list': recommendations
    }
    return render(request, 'designsec/project.html', context)


def generate_recommendation_by_category(request, project=None, category=None):
    """
    Sort the recommendations for a project based on the passed POST parameters
    :param request: HTTP request object containing request metadata
    :param project: The pid that we are looking up (as a hex)
    :return: The rendered webpage
    """
    # todo complete this
    if category is None:
        category = request.GET.get('category', None)

    recommendations, cat_obj = get_recommendation_by_category(cat=category, p_uid=project)
    try:
        url = request.build_absolute_uri(reverse('project_category', kwargs={'project': project, 'category': cat_obj.pk}))
    except NoReverseMatch:
        url = request.build_absolute_uri(reverse('default_category', kwargs={'category': cat_obj.pk}))
    # the url generation is a bit of a hack. It escapes the question mark, so we need to change it back
    # to permalink the get parameter
    url = url.replace('%3F', '?', 1)
    context = {
        'rec_list': recommendations,
        'pid': project,
        'permalink': url
    }
    return render(request, 'designsec/project_recommendations.html', context)


def generate_project_view(request, project=None, category=None):
    """
    Generate the default view for a specified project. If the project cannot be found, a default view will be generated
    :param request: HTTP request object containing request metadata
    :param project: The project to display the information for
    :return: The rendered webpage
    """
    # todo keep track of the number of views and the last view as long as an admin is not logged in (maybe?)

    p_uid = uuid.UUID(project)
    if category is None:
        category = request.GET.get('category', None)
    try:
        p = get_object_or_404(Project, pid=p_uid)
    except Http404:
        subject = 'Security recommendation bad project id {}'.format(project)
        notice = '<strong>Unable to find the reference locator {}.</strong><br />All '.format(project)
        notice += 'recommendations are displayed. Please contact a member of {} '.format(knox.mailto(subject=subject))
        notice += 'if you believe this is a mistake'
        messages.add_message(request, messages.ERROR, notice)
        return generate_default_view(request, category)

    context = {
        'project': p,
        'category': Category.objects.filter(classification__recommendation__project=p).distinct(),
        'category_request': category,
        'pid': project
    }
    return render(request, 'designsec/project.html', context)


# todo ensure that user is properly authenticated before edits happen!

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
    content, status = None, None  # initialization
    # Some operations do not need an ID
    if op == 'add':
        content, status = add_modal(request, target)
    else:
        # The rest need an ID
        t_id = request.POST.get('id', None)
        # make sure that the id is not escaped
        if t_id[:3] == 'pk-':
            t_id = t_id[3:]
        try:
            target_obj = get_object_or_404(SUPPORTED_MODAL_CLASSES[target], pk=t_id)
        except Http404:
            return JsonResponse({'status': '400', 'reason': 'Invalid ID provided'}, status=400)
        if op == 'edit':
            content, status = edit_modal(request, target, target_obj)
        elif op == 'delete':
            content, status = delete_modal(request, target, target_obj)

    safe = False if status != 200 else True
    return JsonResponse(data=content, safe=safe, status=status)


# todo use jquery to get the object we are acting on and the field name for any multi-select.
#       Generate add button dynamically?

# todo when creating a recommendation, make sure that only one classification of each category exists
#   if more than one category, present an error to be more specific and tailor it to one classification.

def add_modal(request, target):
    """
    ADMIN INTERFACE

    This function is used to interact with a modal for adding an instance of the desired target. On the first call,
    the HTML for the modal will be returned. Once that is submitted, we will try to save the data submitted (via POST)

    :param request: HTTP request object containing request metadata.
    :param target: Model target that we are creating an instance for
    :return:
    """
    formset = MODAL_MODEL_FORMS[target]
    if request.POST.get('loaded', None) is not None:
        # we have already been here once, validate and try to save the form
        loaded = formset(request.POST)
        if loaded.is_valid():
            # todo when adding a recommendation, make sure to add it to the 'All' category!
            p = loaded.save()
            messages.add_message(request, messages.SUCCESS, '{} created with id {}'.format(target.capitalize(),
                                                                                           p.pid.hex))
            return {'message': '{} created with id {}'.format(target.capitalize(), p.pid.hex)}, 200

        else:
            return loaded.errors.as_json(), 400
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
    operation_target = 'add{}'.format(target.capitalize())
    response = {
        'form_id': '#{}Form'.format(operation_target),
        'form_button': '#{}Button'.format(operation_target),
        'modal_id': '#{}Modal'.format(operation_target),
        'modal': render_to_string('designsec/admin/modal_generator.html', context, request)
    }
    return response, 200


# todo do we need to be able to specify the action for jquery to perform when modal is closed?

def edit_modal(request, target, edit_target):
    """
    ADMIN INTERFACE

    This function is used to interact with a modal for editing an instance of the desired target. On the first call,
    the HTML for the modal will be returned. Once that is submitted, we will try to save the data submitted (via POST)

    :param request: HTTP request object containing request metadata.
    :param target: Model target that we are editing
    :param edit_target: instantiation of the target that we are editing
    :return:
    """
    # Determine what formset we are trying to show
    formset = MODAL_MODEL_FORMS[target]
    if request.POST.get('loaded', None) is not None:
        # we have already been here once, validate and try to save the form
        loaded = formset(request.POST, instance=edit_target)
        if loaded.is_valid():
            loaded.save()
            return {}, 200
        return loaded.errors.as_json(), 400
    # generate the form for the first time
    context = {
        'operation': 'edit',
        'target': target,
        'formset': formset(instance=edit_target),
        'select_check': '',
        'success_color': 'success',
        'cancel_color': 'danger',
        'id': 'pk-{}'.format(edit_target.pk)
    }
    context.update(MODAL_OPTIONS[target])
    operation_target = 'edit{}'.format(target.capitalize())
    response = {
        'form_id': '#{}Form'.format(operation_target),
        'form_button': '#{}Button'.format(operation_target),
        'modal_id': '#{}Modal'.format(operation_target),
        'modal': render_to_string('designsec/admin/modal_generator.html', context, request)
    }
    return response, 200


def delete_modal(request, target, edit_target):
    """
    ADMIN INTERFACE

    This function is used to interact with a modal for deleting an instance of the desired target. On the first call,
    the HTML for the modal will be returned. Once that is submitted, we will try to delete the instance (via POST)

    :param request: HTTP request object containing request metadata.
    :param target: Model target that we are deleting
    :param edit_target: Instantiation of the target that we are deleting
    :return:
    """
    form = MODAL_MODEL_FORMS[target]
    if request.POST.get('loaded', None) is not None:
        # we have already been here once, validate and try to delete the object
        loaded = form(request.POST, instance=edit_target)
        # todo ensure that this properly protects against deleting 'ALL'
        if loaded.is_valid():
            edit_target.delete()
            return {}, 200
        return loaded.errors.as_json(), 400
    # generate the form for the first time
    f = form(instance=edit_target)
    f.make_readonly()
    # todo figure out why readonly does not work on multi-select -- does this matter?
    context = {
        'operation': 'delete',
        'target': target,
        'formset': f,
        'select_check': '',
        'success_color': 'success',
        'cancel_color': 'danger',
        'id': 'pk-{}'.format(edit_target.pk)
    }
    operation_target = 'delete{}'.format(target.capitalize())
    response = {
        'form_id': '#{}Form'.format(operation_target),
        'form_button': '#{}Button'.format(operation_target),
        'modal_id': '#{}Modal'.format(operation_target),
        'modal': render_to_string('designsec/admin/modal_generator.html', context, request)
    }
    return response, 200


def get_admin_recommendation_by_category(cat=None, p_uid=None):
    """

    :param cat: The id of the recommendation category to sort based on. If none provided, we they will be presented in
                the 'All' category.
    :param p_uid: The project uuid that we are getting the recommendations from. If none provided, we will get
                  all recommendations.
    :return
    """
    # todo complete documentation
    p = get_object_or_404(Project, pid=uuid.UUID(p_uid))
    project_recommendations = p.recommendation.all()

    # get the category that we are trying to display
    try:
        cat_obj = get_object_or_404(Category, id=cat)
    except Http404:
        # If we do not have a valid category, just get the first one defined.
        cat_obj = get_object_or_404(Category, name='All')

    classification_list = []
    # go through all of the classifications for the category and determine if contained recommendations are applied
    # to the current project
    for c in cat_obj.classification_set.order_by('name'):
        rec_list = []
        for r in Recommendation.objects.filter(classification=c).order_by('name'):
            rec_list.append((r, 'checked' if r in project_recommendations else ''))
        classification_list.append((c, rec_list))

    return classification_list, cat_obj


def generate_admin_recommendation_by_category(request, project=None, category=None):
    """
    ADMIN INTERFACE

    Sort the recommendations for a project based on the passed POST parameters
    :param request: HTTP request object containing request metadata
    :param project: The pid that we are looking up (as a hex)
    :return: The rendered webpage
    """
    # todo complete this
    if category is None:
        category = request.GET.get('category', None)

    recommendations, cat_obj = get_admin_recommendation_by_category(cat=category, p_uid=project)

    try:
        url = request.build_absolute_uri(reverse('admin_project_category', kwargs={'project': project, 'category': cat_obj.pk}))
    except NoReverseMatch:
        url = request.build_absolute_uri(reverse('admin_project', kwargs={'category': cat_obj.pk}))
    # the url generation is a bit of a hack. It escapes the question mark, so we need to change it back
    # to permalink the get parameter
    url = url.replace('%3F', '?', 1)
    context = {
        'rec_list': recommendations,
        'category': cat_obj,
        'pid': project,
        'permalink': url
    }
    return render(request, 'designsec/admin/project_recommendations.html', context)


def save_recommendations(request, project=None):
    """
    ADMIN INTERFACE

    :param request:
    :param project:
    :return:
    """
    # todo complete documentation

    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    p = get_object_or_404(Project, pid=uuid.UUID(project))
    update_recommendations = [int(r) for r in request.POST.getlist('recommendation', [])]
    change = set([r.pk for r in p.recommendation.all()]) != set(update_recommendations)

    if change:
        p.recommendation.clear()

        p.recommendation.add(*[r for r in Recommendation.objects.filter(pk__in=update_recommendations)])

        messages.add_message(request, messages.SUCCESS, 'recommendations updated for project {}'.format(p.pid.hex))
    return generate_admin_recommendation_by_category(request, project, request.POST.get('category'))


def generate_admin_project_view(request, project):
    """
    ADMIN INTERFACE

    :param request: HTTP request object containing request metadata
    :param project: Hex representation of target project's UUID
    :return:
    """
    # todo complete this
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

    context = {
        'project': p,
        'category': Category.objects.distinct(),
        'rec_list': get_recommendation_by_category(p_uid=project),
        'pid': project
    }
    return render(request, 'designsec/admin/project.html', context)


# todo change the behavior of list when a delete fires on the admin list - can we remember the last sorting view?
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
            'pid': p.pid.hex,
            'pk': p.pk,
            'added': p.added,
            'modified': p.modified,
            'contact': '; '.join([c.email.split('@')[0] for c in p.contact.order_by('email')]),
            'rec_count': p.recommendation.count(),
            'last_visit': p.last_visit
        }
        context['projects'].append(pr)

    return render(request, 'designsec/admin/list_projects.html', context)
