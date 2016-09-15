from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.db.models import Q
from .models import Post, Category, Tag
import markdown2

class CategoryListView(ListView):

	def get_queryset(self):
		slug = self.kwargs['slug']
		try:
			category = Category.objects.get(slug=slug)
			return Post.objects.filter(category=category)
		except Category.DoesNotExist:
			return Post.objects.none()

	def get_context_data(self, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		slug = self.kwargs['slug']
		try:
			context['category'] = Category.objects.get(slug=slug)
		except Category.DoesNotExist:
			context['category'] = None
		return context

class TagListView(ListView):

	def get_queryset(self):
		slug = self.kwargs['slug']
		try:
			tag = Tag.objects.get(slug=slug)
			return tag.post_set.all()
		except Tag.DoesNotExist:
			return Post.objects.none()

	def get_context_data(self, **kwargs):
		context = super(TagListView, self).get_context_data(**kwargs)
		slug = self.kwargs['slug']
		try:
			context['tag'] = Tag.objects.get(slug=slug)
		except Tag.DoesNotExist:
			context['tag'] = None
		return context

def post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	return render(request, 'blog/jinja2/post.html',{'post':post})

def get_search_results(request):
	"""
	Search for a post by title or text
	"""
	# Retrieve the query data
	query = request.GET.get('q', '')
	page = request.GET.get('page', 1)

	# Query the database
	results = Post.objects.filter(Q(body__icontains=query) | Q(title__icontains=query))
	pages = Paginator(results, 5)

	# Get the page
	try:
		returned_page = pages.page(page)
	except EmptyPage:
		returned_page = pages.page(pages.num_pages)

	return render(request, 'blog/jinja2/search_list.html', {'page_obj': returned_page, 'object_list': returned_page.object_list, 'search': query})

def archive(request):
	categories = Category.objects.all()
	tags = Tag.objects.all()
	return render(request, 'blog/jinja2/archive.html', {'categories': categories, 'tags': tags})

def gallery(request):
	return render(request, 'blog/jinja2/gallery.html')

#def CategoryListView(ListView):
#	category = get_object_or_404(Category, slug=slug)
#	categories = Category.objects.all()
#	posts = Post.objects.filter(categories=category)
#	return render('blog/jinja2/category.html', {'posts':posts})
