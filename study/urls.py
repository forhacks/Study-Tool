from django.conf.urls import url

from . import views

app_name = 'study'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^login/$', views.auth_view, name='auth')
]
