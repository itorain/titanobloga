from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone

class Post(models.Model):
	title = models.CharField(max_length=100, unique=True)
	author = models.ForeignKey('auth.user')
	slug = models.SlugField(unique=True)
	body = models.TextField()
	description = models.TextField(max_length=200)
	publish = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	category = models.ForeignKey('blog.Category', blank=True, null=True)
	updated = models.DateTimeField(db_index=True, blank=True, null=True)
	tags = models.ManyToManyField('blog.Tag')
	
	def __unicode__(self):
		return unicode(self.title)
		
	def publish(self):
		self.publish = True
		self.updated = timezone.now()
		self.save()
		
	def get_absolute_url(self):
		return reverse('blog.views.post', args=[self.slug])
		
	class Meta:
		ordering = ['-updated']	
		
class Category(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
	
	def save(self):
		if not self.slug:
			self.slug = slugify(unicode(self.name))
		super(Category, self).save()
	
	def get_absolute_url(self):
		return "/category/%s" % (self.slug)
	
	def __unicode__(self):
		return self.name
		
	class Meta:
		verbose_name_plural = 'categories'
		
class Tag(models.Model):
	name = models.CharField(max_length=20)
	description = models.TextField(max_length=255, null=True, default='')
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
	
	def save(self):
		if not self.slug:
			self.slug = slugify(unicode(self.name))
		super(Tag, self).save()
		
	def get_absolute_url(self):
		return "/tag/%s/" % (self.slug)
		
	def __unicode__(self):
		return self.name
