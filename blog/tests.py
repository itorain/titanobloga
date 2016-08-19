from django.test import TestCase
from django.utils import timezone
from blog.models import Post
from django.contrib.auth.models import User

# Test cases for the post class
class PostTest(TestCase):
	def test_create_post(self):
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
