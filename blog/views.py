from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag

# Create your views here.
def index(request):
	posts = Post.objects.all()
	return render(request, 'jinja2/index.html',{'posts':posts})
    
def post(request, slug):
	post = get_object_or_404(Post, slug=slug)
	return render(request, 'blog/post.html',{'post':post})

def category_archive(request, slug):
	category = get_object_or_404(Category, slug=slug)
	categories = Category.objects.all()
	posts = Post.objects.filter(categories=category)
	return render('blog/categories.html', {'posts':posts})
    


