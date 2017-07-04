from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.generate_default_view, name='default'),
    url(r'sort/?$', views.generate_recommendation_by_category, name='default_sort'),
    url(r'^(?P<project>[0-1a-zA-Z]{32})/?$', views.generate_project_view, name='project'),
    url(r'^(?P<project>[0-1a-zA-Z]{32})/sort$', views.generate_recommendation_by_category, name='project_sort'),
    url(r'^admin/?$', views.create_new_project, name='create_project'),
    url(r'^admin/(?P<project>[0-1a-zA-Z_\-])/?$', views.edit_project, name='edit_project'),
    url(r'^admin/list/?$', views.list_projects, name='list'),
]
