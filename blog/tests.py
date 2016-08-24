from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag

# Reusable create post function
def create_post():
 # Create the post
	post = Post()
 # Create the author
	try:
		user = User.objects.get(username='mert')
		user.delete()
	except Exception as e:
		user = User.objects.create(username='mert', email='mert@test.com', password='password')
		user.save()
	user, flag = User.objects.get_or_create(username='mert', email='mert@test.com', password='password')
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
		
class AdminTest(LiveServerTestCase):
	fixtures = ['testUsers.json'] # get test user to login
	
	def setUp(self):
	# Create a client
		self.client = Client()
	
	def test_login(self):
	# Get the login page
		response = self.client.get('/admin/', follow=True) # had to add follow to get rid of redirect errors
	# Make sure we got a valid response
		self.assertEquals(response.status_code, 200)		
	# check that we get a login page
		self.assertTrue(b'Log in' in response.content) # had to cast to bytes object
	# Log in 
		self.client.login(username='test', password='notpassword')
		response = self.client.get('/admin/', follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(b'Log out' in response.content)
	# Try logout
		self.client.logout()
		response = self.client.get('/admin/', follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(b'Log in' in response.content)
	
	# TODO fix posts below	
	def test_create_post(self):
		self.client.login(username='test', password='notpassword')
		response = self.client.get('/admin/blog/post/add/')
		self.assertEquals(response.status_code, 200)
	# Create a post
		response = self.client.post('/admin/blog/post/add/', {
			'title': 'test post',
			'author': 'itorain',
			'slug': 'slugtest',
			'body': 'the body of the test post',
			'description': 'test description',	
			'category': 'how-to',	
			'updated_0': '2016-08-12',
			'updated_1': '22:22:23',
			'published': 'True'
		}, follow=True)	
		self.assertEquals(response.status_code, 200)
		#self.assertTrue(b'added successfully' in response.content)
	# Check new post now in database
		#posts = Post.objects.all()
		#self.assertEquals(len(posts), 1)
		
	# TODO fix this
	def test_edit_post(self):
		post = create_post()
		self.client.login(username='test', password='notpassword')
		response = self.client.post('/admin/blog/post/1/', {
			'title': 'changed the title',
			'updated_0': '2016-08-12',
			'updated_1': '22:22:23'
		}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(b'changed successfully' in response.content)
		posts = Post.objects.all()
		self.assertEquals(len(posts), 1)
		only_post = posts[0]
		self.assertEquals(only_post.title, 'changed the title')
	
	# TODO fix this	
	def test_delete_post(self):
		post = create_post()
		self.client.login(username='test', password='notpassword')
		response = self.client.post('/admin/blog/post/1/delete/', {
			'post': 'yes'
		}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(b'deleted successfully' in response.content)
		posts = Post.objects.all()
		self.assertEquals(len(posts), 0)

class PostViewTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()
		
	def test_index(self):
		post = create_post()
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)
	# Check the post title is in the response
		self.assertTrue(post.title in response.content)
    # Check the post text is in the response
		self.assertTrue(post.text in response.content)
    # Check the post date is in the response
		self.assertTrue(str(post.updated.year) in response.content)
		self.assertTrue(post.pub_date.strftime('%b') in response.content)
		self.assertTrue(str(post.updated.day) in response.content)
		
