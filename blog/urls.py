from django.conf.urls import url
from django.views.generic import ListView
from blog.models import Post
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^$', ListView.as_view(model=Post,)),
]
