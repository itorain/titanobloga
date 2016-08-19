from django.test import TestCase
from django.utils import timezone
from blog.models import Post

# Test cases for the post class
class PostTest(TestCase):
	def test_create_post(self):
	# Create the post
		post = Post()
	# Set the attributes	
		post.title = 'Test Post'
		post.body = 'This is a test post!'
		post.created = timezone.now()
		post.updated = timezone.now()
	# Save it
		post.save()
	# Check if I can find post
		allPosts = Post.objects.all()
		self.assertEquals(len(allPosts), 1)
		myPost = allPosts[0]
		self.assertEquals(myPost, post)
	# Check attributes
		self.assertEquals(myPost.title, 'Test Post')
        self.assertEquals(myPost.text, 'This is a test post')
        self.assertEquals(myPost.created.day, post.created.day)
        self.assertEquals(myPost.created.month, post.created.month)
        self.assertEquals(myPost.created.year, post.created.year)
        self.assertEquals(myPost.created.hour, post.created.hour)
        self.assertEquals(myPost.created.minute, post.created.minute)
        self.assertEquals(myPost.created.second, post.created.second)
