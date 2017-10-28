from django.conf.urls import url

from . import views

app_name = 'study'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^auth/$', views.auth_view, name='auth'),
    url(r'^dashboard/$', views.dashboard_view, name='dashboard')
]
