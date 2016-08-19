from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone

class PostManager(models.Manager):
    def all(self):
        return super(PostManager, self).filter(published=True) # will only show posts that are published

class Post(models.Model):
	title = models.CharField(max_length=100, unique=True)
	author = models.ForeignKey('auth.user')
	slug = models.SlugField(unique=True)
	body = models.TextField()
	description = models.TextField(max_length=200)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	category = models.ForeignKey('blog.Category', blank=True, null=True)
	updated = models.DateTimeField(db_index=True, blank=True, null=True)
	published = models.BooleanField(default=False)
	tags = models.ManyToManyField('blog.Tag')
	objects = PostManager()
	
	class Meta:
		ordering = ['-updated']		
	
	def __str__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse('blog.views.post', args=[self.slug])
		
	def publish(self):
		self.published = True
		self.updated = timezone.now()
		self.save()
		
	# Adding a way to next and previous posts for end users	
	def get_previous_post(self):
		return self.get_previous_by_updated()
		
	def get_next_post(self):
		return self.get_next_by_updated()
		
class Category(models.Model):
	name = models.CharField(max_length=50, db_index=True)
	description = models.TextField()
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
	
	class Meta:
		verbose_name_plural = 'categories'
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('blog.views.category', args=[self.slug])	
		
class Tag(models.Model):
	name = models.CharField(max_length=20, db_index=True)
	description = models.TextField(max_length=255, null=True, default='')
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
		
	def __str__(self):
		return self.name		
		
	def get_absolute_url(self):
		return reverse('blog.views.tag', args=[self.slug])
