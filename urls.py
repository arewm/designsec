from django.conf.urls import url

from designsec import views

urlpatterns = [
    url(r'^$', views.redirect_to_default_view),
    # unsorted project viewing interfaces
    url(r'^projects/?$', views.generate_default_view, name='default'),
    url(r'^projects/\?category=(?P<category>\w+)/?$', views.generate_default_view, name='default_category'),
    url(r'^projects/(?P<project>[0-9a-zA-Z]{32})/?$', views.generate_project_view, name='project'),
    # sorted project viewing interfaces
    url(r'^projects/sort/?$', views.generate_recommendation_by_category, name='default_sort'),
    url(r'^projects/(?P<project>[0-9a-zA-Z]{32})/\?category=(?P<category>\w+)/?$',
        views.generate_project_view, name='project_category'),
    url(r'^projects/(?P<project>[0-9a-zA-Z]{32})/sort/?$',
        views.generate_recommendation_by_category, name='project_sort'),
    #
    # admin interfaces
    #

    # unsorted project viewing interfaces
    url(r'^admin/projects/(?P<project>[0-9a-zA-Z_\-]{32})/?$', views.generate_admin_project_view, name='admin_project'),
    # sorted project viewing interfaces
    url(r'^admin/projects/(?P<project>[0-9a-zA-Z]{32})/sort/?$',
        views.generate_admin_recommendation_by_category, name='admin_project_sort'),
    url(r'^admin/projects/(?P<project>[0-9a-zA-Z]{32})/\?category=(?P<category>\w+)/?$',
        views.generate_admin_project_view, name='admin_project_category'),
    # list
    url(r'^admin/projects/?$', views.list_projects, name='list'),
    # utility interfaces
    url(r'^admin/get-modal/(?P<op>(add|edit|delete))/?$', views.get_modal, name='get_modal'),
    url(r'admin/projects/(?P<project>[0-9a-zA-Z]{32})/recommendations/?$',
        views.save_recommendations, name='save_recommendations'),
]
