from django.conf.urls import url
from django.views.generic import ListView, DetailView
from blog.models import Post, Category, Tag
from django.contrib.sitemaps.views import sitemap
from blog.sitemap import PostSitemap, FlatpageSitemap
from . import views

app_name = 'blog'

# Define sitemaps
sitemaps = {
    'posts': PostSitemap,
    'pages': FlatpageSitemap
}

urlpatterns = [
    url(r'^blog/(?P<page>\d+)?/?$', ListView.as_view(model=Post, template_name='blog/jinja2/post_list.html', paginate_by=5), name='post_list'),
    url(r'^blog/(?P<slug>[\w\-]+)/$', DetailView.as_view(model=Post, template_name='blog/jinja2/post.html'), name='post_view'),
    url(r'^blog/category/(?P<slug>[\w\-]+)/$', views.CategoryListView.as_view(model=Category, template_name='blog/jinja2/category_view.html', paginate_by=5), name='category_view'),
    url(r'^blog/tag/(?P<slug>[\w\-]+)/$', views.TagListView.as_view(model=Tag, template_name='blog/jinja2/tag_view.html', paginate_by=5), name='tag_view'),
    url(r'^blog/archive$', views.archive, name='archive'),
    url(r'^blog/search$', views.get_search_results, name='search'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
