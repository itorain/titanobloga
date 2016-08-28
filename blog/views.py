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


# Create your views here.
def post_list(request):
	posts = Post.objects.all().order_by('updated')
	paginator = Paginator(posts, 5)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
	#If the page is not an integer give first page
		posts = paginator.page(1)
	except EmptyPage:
	#If page is out of range
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/jinja2/post_list.html',{'posts':posts})
    
def post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	return render(request, 'blog/jinja2/post.html',{'post':post})
	
def get_search_results(request):
	query = request.GET.get('q', '')
	page = request.GET.get('page', 1)
	
	results = Post.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
	
	pages = Paginator(results, 5)
	
	try:
		returned_page = pages.page(page)
	except EmptyPage:
		returned_page = pages.page(pages.num_pages)
		
	return render(request, 'blog/jinja2/search_list.html', {'page': returned_page, 'posts': returned_page.object_list, 'search': query})

#def CategoryListView(ListView):
#	category = get_object_or_404(Category, slug=slug)
#	categories = Category.objects.all()
#	posts = Post.objects.filter(categories=category)
#	return render('blog/jinja2/category.html', {'posts':posts})
    


