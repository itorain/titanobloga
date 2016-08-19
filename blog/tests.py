from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag

# Reusable create post function
def create_post():
# Create the post
	post = Post()
# Create the author
	user = User.objects.create_user('mert', 'mert@test.com', 'password')
	user.save()
# Set the attributes	
	post.title = 'Test Post'
	post.body = 'This is a test post!'
	post.description = 'a description'
	post.slug = 'test-post'
	post.author = user
	post.created = timezone.now()
	post.updated = timezone.now()
	post.published = True # Need this or Post.objects.all() will filter and will not return this
# Save it
	post.save()
	return post

# Reusable function to create a category
def create_category():
# Create the category
	cat = Category(name='howto', description='how to articles', slug='how-to')
# Save it to db
	cat.save()
	return cat

# Reusable function to create a tag
def create_tag():
# Create a tag	
	tag = Tag(name='diy', description='diy articles', slug='diy')
# Save it to db
	tag.save()
	return tag

# Test cases for the post class
class PostTest(TestCase):
	def test_create_post(self):
	# Create the post
		post = create_post()
	# Check if I can find post
		allPosts = Post.objects.all()
		self.assertEquals(len(allPosts), 1)
		myPost = allPosts[0]
		self.assertEquals(myPost, post)
	# Check attributes
		self.assertEquals(myPost.title, 'Test Post')
		self.assertEquals(myPost.body, 'This is a test post!')
		self.assertEquals(myPost.description, 'a description')
		self.assertEquals(myPost.slug, 'test-post')
		self.assertEquals(myPost.author.username, 'mert')
		self.assertEquals(myPost.author.email, 'mert@test.com')
		self.assertEquals(myPost.created.day, post.created.day)
		self.assertEquals(myPost.created.month, post.created.month)
		self.assertEquals(myPost.created.year, post.created.year)
		self.assertEquals(myPost.created.hour, post.created.hour)
		self.assertEquals(myPost.created.minute, post.created.minute)
		self.assertEquals(myPost.created.second, post.created.second)
		
class CategoryTest(TestCase):
	def test_create_category(self):
		cat = create_category()
	# Check category
		allCats = Category.objects.all()
		self.assertEquals(len(allCats), 1)
		myCat = allCats[0]
		self.assertEquals(myCat, cat)
		self.assertEquals(myCat.name, 'howto')
		self.assertEquals(myCat.description, 'how to articles')
		self.assertEquals(myCat.slug, 'how-to')
	# Check assigning to a post
		post = create_post()
		post.save()
		count = Post.objects.count()
		self.assertEquals(count, 1)
		post.category = cat
		post.save()
		p = Post.objects.get(id=1)
		self.assertEquals(p.category, cat)
		
class TagTest(TestCase):
	def test_create_tag(self):
		tag = create_tag()
	# Check tag
		allTags = Tag.objects.all()
		self.assertEquals(len(allTags), 1)
		myTag = allTags[0]
		self.assertEquals(myTag, tag)
		self.assertEquals(myTag.name, 'diy')
		self.assertEquals(myTag.description, 'diy articles')
		self.assertEquals(myTag.slug, 'diy')
	# Check assigning to a post
		post = create_post()
		post.save()
		count = Post.objects.count()
		self.assertEquals(count, 1)
		post.tags.add(tag)
		post.save()
		p = Post.objects.get(id=1)
		post_tags = p.tags.all()
		self.assertEquals(len(post_tags), 1)
		only_post_tag = post_tags[0]
		self.assertEquals(only_post_tag, tag)
		self.assertEquals(only_post_tag.name, 'diy')
		self.assertEquals(only_post_tag.description, 'diy articles')
