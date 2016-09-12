from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models.signals import post_save
#from django.core.cache import cache

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
	site = models.ForeignKey(Site)
	updated = models.DateTimeField(blank=True, null=True)
	published = models.BooleanField(default=False)
	tags = models.ManyToManyField('blog.Tag', blank=True)
	objects = PostManager()

	class Meta:
		ordering = ['-updated']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_view', args=[self.slug])

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(str(self.name))
		super(Post, self).save(*args, **kwargs)


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
		return reverse('blog:category_view', args=[self.slug])

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(str(self.name))
		super(Category, self).save(*args, **kwargs)

class Tag(models.Model):
	name = models.CharField(max_length=20, db_index=True)
	description = models.TextField(max_length=255, null=True, default='')
	slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('blog:tag_view', args=[self.slug])

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(str(self.name))
		super(Tag, self).save(*args, **kwargs)

# Define signals
#def new_post(sender, instance, created, **kwargs):
	#cache.clear()

# Set up signals
#post_save.connect(new_post, sender=Post)
