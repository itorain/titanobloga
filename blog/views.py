from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.db.models import Q
from .models import Post, Category, Tag
import markdown2

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

@api_view(['GET'])
def api(request):
	if request.method == 'GET':
		payload = {'Name':'Isaiah Torain',
			'Address': '850 South Overland Trail #28, Fort Collins, Colorado 80521',
			'Phone':'719-761-9917',
			'Email':'Isaiah.Torain@Outlook.com',
			'Programming-languages': ['Python', 'Java', 'C#', 'JavaScript', 'C++'],
			'Skills': ['Bash and Shell scripting', 'Object-Oriented Programming', 'Test Driven development', 'Unit Testing with optimal code coverage', 'Data Analysis using Hadoop and Neural Networks', 'Full Stack Web Development', 'Agile/Scrum'],
			'Work-history': {
				'New Belgium Brewing': {
					'Location': 'Fort Collins, CO',
					'Title': 'Web Development Intern',
					'Dates': 'April 2015 - Now',
					'Work': 'Developed powershell script to automate coworker account creation, reducing time spent creating new coworker accounts by 25%. Developed Interactive Voice Response phone application for product production related emergencies using Twilio API to cut costs by 20%. Used Model-View-Controller C# framework to create internal web application to manage emergency on call system. Integrated Twilio and MVC web application with Microsoft Team Foundation Server for Agile type development and continuous integration builds achieving 95% code coverage.'
				},
				'ViaSat Inc': {
					'Location': 'Denver, CO',
					'Title': 'Network Solutions Engineer - Intern',
					'Dates': 'May 2016 - August 2016',
					'Work': 'Developed, tested, and deployed Bayesian Network based Risk Analysis Tool for use in a new continuous integration/deployment pipeline in a complex satellite network architecture. Collaborated with small team in a Scrum development framework to create Risk Analysis tool. Integrated Python with several external data sources and APIs such as Splunk to create Risk Analysis tool. Applied machine learning concepts to clean existing data and collect new data to train Bayesian Model. Used Jira and Docker to deploy application to production environment.'
				},
				'Encompass Technologies': {
					'Location': 'Fort Collins, CO',
					'Title': 'Software Development Intern',
					'Dates': 'February 2016 - May 2016',
					'Work': 'Maintained code that facilitated the transfer of Electronic Data Information to and from external customer systems. using XML translation files. Built and tested a paginated, dynamic query response web page. Capitalized on Javascript\'s asynchronous abilities to validate user inforSmation entered against a database.'
				}
			},
			'Education': {
				'School': 'Colorado State University, - Fort Collins, CO',
				'Major': 'Computer Science',
				'Minor': 'Mathematics',
				'Coursework': ['Software Development', 'Computer Security', 'Algorithms', 'Machine Learning', 'Databases', 'Big Data', 'Parallel Programming'],
				'Extracurriculars': 'National Security of Black Engineers'
			},
			'Projects': ['https://github.com/itorain/EventBrite-event-finder', 'https://github.com/itorain/Android-Quiz-App', 'This api/website']
		}
		return Response(payload, status=200, content_type='application/json')
	else:
		 return Response(status=405)


#def CategoryListView(ListView):
#	category = get_object_or_404(Category, slug=slug)
#	categories = Category.objects.all()
#	posts = Post.objects.filter(categories=category)
#	return render('blog/jinja2/category.html', {'posts':posts})
