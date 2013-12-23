from django.conf.urls import patterns, url
from django.views import generic

from .models import Motion

urlpatterns = patterns('',
    url(r'^$', generic.ListView.as_view(model=Motion), name='motion_list'),
    url(r'^(?P<pk>m\d{8}\.\d+)/$', generic.DetailView.as_view(model=Motion), name='motion_detail')
)