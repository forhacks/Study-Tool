from django.conf.urls import url, include

from . import views

app_name = 'study'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard/', include([
        url(r'^$', views.DashboardView.as_view(), name='index'),
        url(r'^new/$', views.NewDeckView.as_view(), name='new'),
        url(r'^deck/(?P<pk>[0-9]+)/', include([
            url(r'^$', views.DeckView.as_view(), name='index')
        ], namespace='deck'))
    ], namespace='dashboard'))
]
