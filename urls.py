from django.conf.urls import url

from designsec import views

urlpatterns = [
    url(r'^$', views.generate_default_view, name='default'),
    url(r'^sort/?$', views.generate_recommendation_by_category, name='default_sort'),
    url(r'^(?P<project>[0-9a-zA-Z]{32})/?$', views.generate_project_view, name='project'),
    url(r'^(?P<project>[0-9a-zA-Z]{32})/sort$', views.generate_recommendation_by_category, name='project_sort'),
    url(r'^admin/(?P<project>[0-9a-zA-Z_\-]{32})/?$', views.generate_edit_project_view, name='edit_project'),
    url(r'^admin/list/?$', views.list_projects, name='list'),
    url(r'^admin/get-modal/(?P<op>(add|edit|delete))/?$', views.get_modal, name='get_modal'),
]
