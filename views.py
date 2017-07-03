# Generate a view by sorting on a specific category
# Generate a view for the admin where you can 

# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse, HttpResponse, Http404
# from django.db.models import Q
# from django.forms.models import model_to_dict
#
# from .models import Tag, Person, Action, PolicyAction, Policies, PolicyTag, TagCategory
#
# from random import random, randint, choice, sample
# import re
#
# is_test = False
# default_id = 'c54de108-7cf1-493c-912d-a4ddb990a185' if is_test else None
# system = Person.objects.filter(person_id='00000000-0000-0000-0000-000000000000')[0]
#
#
# def index(request):
#     context = {}
#     return render(request, 'survey/index.html', context)
#
#
# def consent(request):
#     return render(request, 'survey/consent.html', {})
#
#
# def tutorial(request):
#     # If they did not accept the consent, redirect them to an end message.
#     consent_accepted = request.POST.get('agree', 'no') == 'yes'
#     if is_test:
#         consent_accepted = True
#     if not consent_accepted:
#         return redirect('end')
#     # Create the user for this instance. Randomly assign them to expert or non-expert.
#     expert = random() < 0.5
#     if is_test:
#         p = Person.objects.get(person_id=default_id)
#         expert = bool(request.GET.get('e', 0))
#     else:
#         p = Person(expert=expert, consent_accepted=consent_accepted)
#         p.save()
#
#     # Make sure we set some kind of cookie here to determine if they have completed the survey.
#     #   maybe allow the user to pick up where they left off...? probably not now.
#     context = {'expert': expert, 'person': p.person_id}
#     return render(request, 'survey/tutorial.html', context)
#
#
# def add_system_policy(request):
#     p=None
#     if request.GET.get('long_securitybyObsc.3tyPhrasetha18tIsjus-~hIBLE', None) is not None:
#         p = system
#
#     policy_sugg_owner = system
#     if is_test:
#         is_expert = bool(request.GET.get('e', 0))
#         policy_sugg_owner = None if is_expert else p
#
#     # Get all system defaults to populate the page with
#     actions = Action.objects.all()
#     action_list = []
#     for a in actions:
#         action_list.append(('a{}'.format(a.action_id), a.text))
#     categories = TagCategory.objects.order_by('display_order')
#     tag_list = []
#     for c in categories:
#         tags = Tag.objects.filter(tag_cat=c).filter(Q(creator=None) | Q(creator=policy_sugg_owner)).order_by('text')
#         for t in tags:
#             t.tag_id = 't{}'.format(t.tag_id)
#         tag_list.append((c, tags))
#     # Get the suggested policies if we want to display them.
#     expert_policies = Policies.objects.filter(owner=policy_sugg_owner)
#     sugg_policies = []
#     for e in expert_policies:
#         this_policy = []
#         for t in e.tags.all():
#             this_policy.append((t.tag_cat.name, 't{}'.format(t.tag_id), t.text))
#         sugg_policies.append(('p{}'.format(e.policy_id), this_policy))
#     # make the context for generating the page
#     context = {'person': p.person_id,
#                'actions': action_list,
#                'categories': categories,
#                'tags': tag_list,
#                'policies': sugg_policies}
#     return render(request, 'survey/policy.html', context)
#
# def policy(request):
#     # Determine who is creating policies
#     p = get_object_or_404(Person, person_id=request.POST.get('person', default_id))
#
#     policy_sugg_owner = None if p.expert else system
#     if is_test:
#         is_expert = bool(request.GET.get('e', 0))
#         policy_sugg_owner = None if is_expert else p
#
#     # Get all system defaults to populate the page with
#     actions = Action.objects.all()
#     action_list = []
#     for a in actions:
#         action_list.append(('a{}'.format(a.action_id), a.text))
#     categories = TagCategory.objects.order_by('display_order')
#     tag_list = []
#     for c in categories:
#         tags = Tag.objects.filter(tag_cat=c).filter(Q(creator=None) | Q(creator=policy_sugg_owner)).order_by('text')
#         for t in tags:
#             t.tag_id = 't{}'.format(t.tag_id)
#         tag_list.append((c, tags))
#     # Get the suggested policies if we want to display them.
#     expert_policies = Policies.objects.filter(owner=policy_sugg_owner)
#     sugg_policies = []
#     for e in expert_policies:
#         this_policy = []
#         for t in e.tags.all():
#             this_policy.append((t.tag_cat.name, 't{}'.format(t.tag_id), t.text))
#         sugg_policies.append(('p{}'.format(e.policy_id), this_policy))
#     # make the context for generating the page
#     context = {'person': p.person_id,
#                'actions': action_list,
#                'categories': categories,
#                'tags': tag_list,
#                'policies': sugg_policies}
#     return render(request, 'survey/policy.html', context)
#
#
# def submit_policy(request):
#     p = get_object_or_404(Person, person_id=request.POST.get('person', default_id))
#     is_generated = request.POST.get('gen', None) is not None
#     new_policy = Policies(owner=p, time_to_generate=request.POST.get('time', '-1'), generated=is_generated)
#     # todo allow policy to be skipped (for policy generator)
#     generate_new_policy = request.POST.get('get_another', None) is not None
#
#     tag_list = [get_object_or_404(Tag, tag_id=t[1:]) for t in request.POST.getlist('tag')]
#
#     # get GUIDs by removing the first character
#     action_list = [a[1:] for a in request.POST.getlist('action')]
#     for a in Action.objects.all():
#         # Create the necessary PolicyAction if it does not exist
#         allowed = str(a.action_id) in action_list
#         try:
#             act = get_object_or_404(PolicyAction, action_id=a, allow=allowed)
#         except Http404:
#             act = PolicyAction(action_id=a, allow=allowed)
#             act.save()
#         # add the policy actions to the new policy
#         new_policy.actions.add(act)
#
#         action_tags = PolicyTag.objects.filter(owner=p).filter(action=a)
#         for t in tag_list:
#             if not action_tags.filter(tag=t):
#                 pt = PolicyTag(tag=t, owner=p, action=a)
#                 pt.save()
#
#     new_policy.tags.add(*tag_list)
#     new_policy.save()
#
#     response = {'id': new_policy.policy_id, 'num': Policies.objects.count()}
#     if generate_new_policy:
#         more, percent = need_more_policies(p)
#         if more:
#             response['tags'], response['categories'] = generate_policy(p)
#         else:
#             response['tags'] = []
#             response['categories'] = []
#         response['more'] = not not response['tags']
#         response['percent'] = int(percent)
#     return JsonResponse(response)
#
#
# def remove_policy(request):
#     # do something like this to see if the tags are associated with any other policies...
#     # if user.partner_set.filter(slug=requested_slug).exists():
#     # use .delete()
#     #
#     # Probably not going to happen soon. There has to be a lot of upkeep to make sure that
#     # stuff is only deleted that is not being referenced anymore.
#     # If we want to do it, investigate the policies_all() method on the PolicyAction and PolicyTag to see
#     # if there are any more policies referencing the object in a ManyToMany field.
#     pass
#
#
# def custom_tag(request):
#     # create a custom tag as long as it does not already exist as a system or this-user tag
#     response = {'new': 'false', 'category': request.POST['category']}
#     p = get_object_or_404(Person, person_id=request.POST.get('person', default_id))
#     category = get_object_or_404(TagCategory, name=request.POST['category'])
#     if not Tag.objects.filter(Q(text=request.POST['tag'].strip()) &
#                               Q(tag_cat=category) &
#                               (Q(creator=None) | Q(creator=p))):
#         # we cannot find a system or user-created tag with the text and class provided
#         tag = Tag(text=request.POST['tag'].strip(), tag_cat=category, custom=True, creator=p)
#         tag.save()
#         response['new'] = 'true'
#         response['id'] = 't{}'.format(tag.tag_id)
#         response['text'] = tag.text
#     return JsonResponse(response)
#
#
# def custom_tag_order(tag):
#     return '{} {} {}'.format(tag.tag_cat.display_order, tag.tag_cat.name, tag.text)
#
#
# def rank(request):
#     p = get_object_or_404(Person, person_id=request.POST.get('person', default_id))
#
#     action_number = int(request.POST.get('action', '0'))
#     a = Action.objects.all()[action_number:action_number+1]
#     if not a:
#         # if we have no more actions, go to the policy generator
#         return redirect('gen')
#     a = a[0]
#
#     tag_list = [pt.tag for pt in PolicyTag.objects.filter(owner=p, action=a)]
#     tag_list.sort(key=custom_tag_order)
#     for t in tag_list:
#         t.tag_id = 'a{}'.format(t.tag_id)
#     ids = re.sub(r'[\'"]', '', str(['#{}'.format(t.tag_id) for t in tag_list])[1:-1])
#     insert_list = []
#     class_dict = {0: 'first', 1: 'second', 2: 'third', 3: 'fourth'}
#     i = 0
#     for t in tag_list:
#         insert_list.append((class_dict[i % 4], t))
#         i += 1
#     action_number += 1
#     context = {'person': p.person_id,
#                'tags': insert_list,
#                'ids': ids,
#                'number': len(tag_list),
#                'action': a,
#                'next_action': action_number,
#                'percent': int(action_number/Action.objects.count()*100)}
#     return render(request, 'survey/rank.html', context)
#
#
# def save_rank(request):
#     p = get_object_or_404(Person, person_id=request.POST.get('person', default_id))
#     a = get_object_or_404(Action, action_id=request.POST.get('action', None))
#
#     tag = get_object_or_404(Tag, tag_id=request.POST.get('tag')[1:])
#
#     my_tag = get_object_or_404(PolicyTag, owner=p, tag=tag, action=a)
#     my_tag.priority = int(request.POST.get('rank', '-1'))
#     my_tag.save()
#     return HttpResponse('')
#
#
# def gen(request):
#     p = get_object_or_404(Person, person_id=request.POST.get('person', default_id))
#
#     actions = Action.objects.all()
#     action_list = []
#     for a in actions:
#         action_list.append(('a{}'.format(a.action_id), a.text))
#
#     more, percent = need_more_policies(p)
#     context = {'person': p, 'actions': action_list, 'tags': {}, 'percent': int(percent)}
#     context['type'] = 'e' if p.expert else 'n'
#     if more:
#         context['tags'], context['categories'] = generate_policy(p)
#     return render(request, 'survey/generate.html', context)
#
#
# def need_more_policies(p):
#     num_created = Policies.objects.filter(owner=p).filter(generated=False).count()
#     num_generated = Policies.objects.filter(owner=p).filter(generated=True).count()
#     if num_created == 0:
#         return False, 0
#     percent = min(num_generated/num_created, 1)*100
#     return percent < 100, percent
#
#
# def verify_policy(p, policy):
#     search = Policies.objects.filter(owner=p)
#     for np in policy:
#         search = search & np.policies_set.all()
#     if search:
#         for s in search:
#             if s.tags.all().count == len(policy):
#                 return False
#     return True
#
#
# def generate_policy(p):
#     t = [t['tags'] for t in Policies.objects.filter(owner=p).values('tags').distinct()]
#     t_cats = [c for c in Tag.objects.filter(tag_id__in=t).values('tag_cat').distinct()]
#     ntags = randint(2, 3)
#     new_policy = []
#     categories = []
#     i = 0
#     if len(t_cats) >= ntags:
#         # we have enough categories to ensure each is unique
#         while i < 5:
#             i += 1
#             cats = sample(t_cats, ntags)
#             for c in cats:
#                 new_policy.append(choice(Tag.objects.filter(tag_id__in=t).filter(tag_cat=c['tag_cat'])))
#             # We have a potential policy, test to see if it exists.
#             # get the intersection of policies that contain each filter
#             if verify_policy(p, new_policy):
#                 categories = [TagCategory.objects.get(pk=c['tag_cat']) for c in cats]
#                 break
#             else:
#                 new_policy.clear()
#     else:
#         policy_tags = Tag.objects.filter(tag_id__in=t)
#         while i < 5:
#             i += 1
#             # five attempts to find a policy suggestion
#             while len(new_policy) < ntags:
#                 # find three unique tags
#                 selection = choice(policy_tags)
#                 if selection not in new_policy:
#                     new_policy.append(selection)
#             # We have a potential policy, test to see if it exists.
#             # get the intersection of policies that contain each filter
#             if not verify_policy(p, new_policy):
#                 new_policy.clear()
#             if new_policy:
#                 # hooray, we still have a new policy!
#                 # make sure we do not have two of any category
#                 done = True
#                 for t in new_policy:
#                     c = t.tag_cat
#                     if c in categories:
#                         if c.name == 'time' or c.name == 'location':
#                             done = False
#                     else:
#                         categories.append(c)
#                 if done:
#                     break
#                 else:
#                     categories.clear()
#                     new_policy.clear()
#     return_tags = []
#     for t in new_policy:
#         return_tags.append(model_to_dict(t))
#         return_tags[-1]['tag_id'] = 't{}'.format(t.tag_id)
#         return_tags[-1]['category'] = t.category
#     return_categories = []
#     for c in categories:
#         return_categories.append(model_to_dict(c))
#     return return_tags, return_categories
#
#
# def next_generated_policy(request):
#     if is_test:
#         p = Person.objects.get(person_id=default_id)
#     else:
#         p = get_object_or_404(Person, person_id=request.POST.get('person', None))
#
#     response = dict()
#     response['tags'], response['categories'] = generate_policy(p)
#     return JsonResponse(response)
#
#
# def end(request):
#     context = {}
#     return render(request, 'survey/end.html', context)
