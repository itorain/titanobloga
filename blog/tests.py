from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.contrib.flatpages.models import FlatPage
import markdown2 as markdown
import factory.django

# Factories for tests
class SiteFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Site
		django_get_or_create = (
			'name',
			'domain'
		)
	name = 'localhost'
	domain = '127.0.0.1:8000'

class CategoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Category
		django_get_or_create = (
			'name',
			'description',
			'slug'
		)

	name = 'how to'
	description = 'How to articles'
	slug = 'howto'

class TagFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Tag
		django_get_or_create = (
			'name',
			'description',
			'slug'
		)

	name = 'diy'
	description = 'diy articles'
	slug = 'diy'

class AuthorFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
		django_get_or_create = (
			'username',
			'email',
			'password'
		)

	username = 'mert1'
	email = 'mert1@test.com'
	password = 'notpassword'

class PostFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Post
		django_get_or_create = (
			'title',
			'body',
			'description',
			'slug',
			'created',
			'updated',
			'published'
		)

	title = 'Test Post'
	body = 'This is a test post!'
	description = 'a description'
	slug = 'test-post'
	created = timezone.now()
	updated = timezone.now()
	published = True # Need this or Post.objects.all() will filter and will not return this
	author = factory.SubFactory(AuthorFactory)
	site = factory.SubFactory(SiteFactory)
	category = factory.SubFactory(CategoryFactory)

class FlatPageFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = FlatPage
		django_get_or_create = (
			'url',
			'title',
			'content'
		)

	url = '/about/'
	title = 'About me'
	content = 'All about me'

# Test cases for the post class
class PostTest(TestCase):

	# Test case to ensure creating a category
	def test_create_category(self):
		cat = CategoryFactory()
	# Check category
		allCats = Category.objects.all()
		self.assertEqual(len(allCats), 1)
		myCat = allCats[0]
		self.assertEqual(myCat, cat)
		self.assertEqual(myCat.name, 'how to')
		self.assertEqual(myCat.description, 'How to articles')
		self.assertEqual(myCat.slug, 'howto')

	# Test case to ensure creating a tag
		def test_create_tag(self):
			tag = TagFactory()
		# Check tag
			allTags = Tag.objects.all()
			self.assertEqual(len(allTags), 1)
			myTag = allTags[0]
			self.assertEqual(myTag, tag)
			self.assertEqual(myTag.name, 'diy')
			self.assertEqual(myTag.description, 'diy articles')
			self.assertEqual(myTag.slug, 'diy')

	def test_create_post(self):
	# Create the post
		post = PostFactory()
	# Check if I can find post
		allPosts = Post.objects.all()
		self.assertEqual(len(allPosts), 1)
		myPost = allPosts[0]
		self.assertEqual(myPost, post)
	# Add a tag
		tag = TagFactory()
		post.tags.add(tag)
	# Check attributes
		self.assertEqual(myPost.title, 'Test Post')
		self.assertEqual(myPost.body, 'This is a test post!')
		self.assertEqual(myPost.description, 'a description')
		self.assertEqual(myPost.slug, 'test-post')
		self.assertEqual(myPost.site.name, 'localhost')
		self.assertEqual(myPost.site.domain, '127.0.0.1:8000')
		self.assertEqual(myPost.author.username, 'mert1')
		self.assertEqual(myPost.author.email, 'mert1@test.com')
		self.assertEqual(myPost.created.day, post.created.day)
		self.assertEqual(myPost.created.month, post.created.month)
		self.assertEqual(myPost.created.year, post.created.year)
		self.assertEqual(myPost.created.hour, post.created.hour)
		self.assertEqual(myPost.created.minute, post.created.minute)
		self.assertEqual(myPost.created.second, post.created.second)
		self.assertEqual(myPost.category.name, 'how to')
		self.assertEqual(myPost.category.description, 'How to articles')

		# Check tags
		ptags = myPost.tags.all()
		self.assertEqual(len(ptags), 1)
		ptag = ptags[0]
		self.assertEqual(ptag, tag)

class BaseAcceptanceTest(LiveServerTestCase):
	def setUp(self):
		self.client = Client()

class AdminTest(BaseAcceptanceTest):
	fixtures = ['testUsers.json'] # get test user to login

	def test_login_logout(self):
	# Get the login page
		response = self.client.get('/admin/', follow=True) # had to add follow to get rid of redirect errors
	# Make sure we got a valid response
		self.assertEqual(response.status_code, 200)
	# check that we get a login page
		self.assertTrue(b'Log in' in response.content) # had to cast to bytes object
	# Log in
		self.client.login(username='test', password='notpassword')
		response = self.client.get('/admin/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'Log out' in response.content)
	# Try logout
		self.client.logout()
		response = self.client.get('/admin/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'Log in' in response.content)

	def test_create_category(self):
	# Log in
		self.client.login(username='test', password='notpassword')
	# Check response code
		response = self.client.get('/admin/blog/category/add/')
		self.assertEqual(response.status_code, 200)
	# Create the new category
		response = self.client.post('/admin/blog/category/add/', {
			'name': 'how to',
			'description': 'How to articles'
			},
			follow=True
		)
		self.assertEqual(response.status_code, 200)
	# Check added successfully
		self.assertTrue(b'added successfully' in response.content)
	# Check new category is in database
		all_cats = Category.objects.all()
		self.assertEqual(len(all_cats), 1)

	def test_edit_category(self):
		cat = CategoryFactory()
	# Log in
		self.client.login(username='test', password='notpassword')
	# Edit the category
		response = self.client.post('/admin/blog/category/' + str(cat.pk) + '/change/', {
			'name': 'python',
			'description': 'The python programming language'
			},
			follow=True
		)
	# Check successful change
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'changed successfully' in response.content)
		all_cats = Category.objects.all()
		self.assertEqual(len(all_cats), 1)
		myCat = all_cats[0]
		self.assertEqual(myCat.name, 'python')
		self.assertEqual(myCat.description, 'The python programming language')

	def test_delete_category(self):
		category = CategoryFactory()
		self.client.login(username='test', password='notpassword')
	# Delete the category
		response = self.client.post('/admin/blog/category/' + str(category.pk) + '/delete/', {
			'post':'yes'
			},
			follow=True
		)
	# Check successful delete
		self.assertTrue(b'deleted successfully' in response.content)
	# Check category deleted
		all_cats = Category.objects.all()
		self.assertEqual(len(all_cats), 0)

	def test_create_tag(self):
	# Log in
		self.client.login(username='test', password='notpassword')
	# Check response code
		response = self.client.get('/admin/blog/tag/add/')
		self.assertEqual(response.status_code, 200)
	# Create the new tag
		response = self.client.post('/admin/blog/tag/add/', {
			'name': 'diy',
			'description': 'diy articles'
			},
			follow=True
		)
		self.assertEqual(response.status_code, 200)
	# Check added successfully
		self.assertTrue(b'added successfully' in response.content)
	# Check new tag is in database
		all_tags = Tag.objects.all()
		self.assertEqual(len(all_tags), 1)

	def test_edit_tag(self):
		tag = TagFactory()
	# Log in
		self.client.login(username='test', password='notpassword')
	# Edit the tag
		response = self.client.post('/admin/blog/tag/' + str(tag.pk) + '/change/', {
			'name': 'python',
			'description': 'The python programming language'
			},
			follow=True
		)
	# Check successful change
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'changed successfully' in response.content)
		all_tags = Tag.objects.all()
		self.assertEqual(len(all_tags), 1)
		myTag = all_tags[0]
		self.assertEqual(myTag.name, 'python')
		self.assertEqual(myTag.description, 'The python programming language')

	def test_delete_tag(self):
		tag = TagFactory()
		self.client.login(username='test', password='notpassword')
	# Delete the tag
		response = self.client.post('/admin/blog/tag/' + str(tag.pk) + '/delete/', {
			'post':'yes'
			},
			follow=True
		)
	# Check successful delete
		self.assertTrue(b'deleted successfully' in response.content)
	# Check tag deleted
		all_tags = Tag.objects.all()
		self.assertEqual(len(all_tags), 0)

	def test_create_post(self):
		category = CategoryFactory()
		tag = TagFactory()
		self.client.login(username='test', password='notpassword')
		response = self.client.get('/admin/blog/post/add/')
		self.assertEqual(response.status_code, 200)
	# Create a post
		response = self.client.post('/admin/blog/post/add/', {
			'title': 'Test Post',
			'slug': 'test-post',
			'body': 'This is a test post!',
			'description': 'a description',
			'category': str(category.pk),
			'created_0': '2016-08-12',
			'created_1': '22:22:23',
			'updated_0': '2016-08-12',
			'updated_1': '22:22:23',
			'site': '2',
			'published': 'True',
			'author': '1',
			'tags': str(tag.pk)
			},
			follow=True
		)
		self.assertEqual(response.status_code, 200)
	# Check successful post
		#print (response.content.decode('utf-8'))
		self.assertTrue(b'added successfully' in response.content)
	# Check new post now in database
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)

	def test_create_post_without_tag(self):
		category = CategoryFactory()
		self.client.login(username='test', password='notpassword')
		response = self.client.get('/admin/blog/post/add/')
		self.assertEqual(response.status_code, 200)
	# Create a post
		response = self.client.post('/admin/blog/post/add/', {
			'title': 'Test Post',
			'slug': 'test-post',
			'body': 'This is a test post!',
			'description': 'a description',
			'category': str(category.pk),
			'created_0': '2016-08-12',
			'created_1': '22:22:23',
			'updated_0': '2016-08-12',
			'updated_1': '22:22:23',
			'site': '2',
			'published': 'True',
			'author': '1'
			},
			follow=True
		)
		self.assertEqual(response.status_code, 200)
	# Check successful post
		self.assertTrue(b'added successfully' in response.content)
	# Check new post now in database
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)

	def test_edit_post(self):
		post = PostFactory()
		category = CategoryFactory()
		tag = TagFactory()
		post.tags.add(tag)
		self.client.login(username='test', password='notpassword')
		response = self.client.post('/admin/blog/post/' + str(post.pk) + '/change/', {
			'title': 'changed the title',
			'slug': 'changed-the-title',
			'body': 'this is a change of the original',
			'description': 'a description',
			'category': str(category.pk),
			'created_0': '2016-08-12',
			'created_1': '22:22:23',
			'updated_0': '2016-08-12',
			'updated_1': '22:22:23',
			'site': '2',
			'published': 'True',
			'author': '1',
			'tags': str(tag.pk)
			},
			follow=True
		)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'changed successfully' in response.content)
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)
		myPost = posts[0]
		self.assertEqual(myPost.title, 'changed the title')

	def test_delete_post(self):
		post = PostFactory()
		tag = TagFactory()
		post.tags.add(tag)
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)
		self.client.login(username='test', password='notpassword')
		response = self.client.post('/admin/blog/post/' + str(post.pk) + '/delete/', {
			'post': 'yes'
			},
			follow=True
		)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(b'deleted successfully' in response.content)
		posts = Post.objects.all()
		self.assertEqual(len(posts), 0)

class PostViewTest(BaseAcceptanceTest):
	def text_index(self):
	# Create the post
		post = PostFactory(body='This is [my first blog post](http://127.0.0.1:8000/)')
    # Create the tag
		tag = TagFactory(name='python', description='Python programming language')
		post.tags.add(tag)
    # Check new post saved
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)
    # Fetch the index
		response = self.client.get(reverse('blog:post_list'))
		self.assertEqual(response.status_code, 200)
    # Check the post title is in the response
		self.assertTrue(post.title in response.content.decode('utf-8'))
    # Check the post text is in the response
		self.assertTrue(markdown.markdown(post.body) in response.content.decode('utf-8'))
    # Check the post category is in the response
		self.assertTrue(post.category.name in response.content.decode('utf-8'))
    # Check the post tag is in the response
		post_tag = posts[0].tags.all()[0]
		self.assertTrue(post_tag.name in response.content.decode('utf-8'))
    # Check the post date is in the response
		self.assertTrue(str(post.updated.year) in response.content.decode('utf-8'))
		self.assertTrue(post.updated.strftime('%b') in response.content.decode('utf-8'))
		self.assertTrue(str(post.updated.day) in response.content.decode('utf-8'))
    # Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content.decode('utf-8'))
    # Check the correct template was used
		self.assertTemplateUsed(response, 'blog/jinja2/post_list.html')

	def test_post_page(self):
		post = PostFactory(body='This is [my first blog post](http://127.0.0.1:8000/)')
		tag = TagFactory(name='python', description='Python programming language')
		post.tags.add(tag)
    # Check new post saved
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)
		myPost = posts[0]
		self.assertEqual(myPost, post)
    # Get the post URL
		url = myPost.get_absolute_url()
    # Fetch the post
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
    # Check the post title is in the response
		self.assertTrue(post.title in response.content.decode('utf-8'))
    # Check the post category is in the response
		self.assertTrue(post.category.name in response.content.decode('utf-8'))
    # Check the post tag is in the response
		myTag = posts[0].tags.all()[0]
		self.assertTrue(myTag.name in response.content.decode('utf-8'))
    # Check the post text is in the response
		self.assertTrue(markdown.markdown(post.body) in response.content.decode('utf-8'))
    # Check the post date is in the response
		self.assertTrue(str(post.updated.year) in response.content.decode('utf-8'))
		self.assertTrue(post.updated.strftime('%b') in response.content.decode('utf-8'))
		self.assertTrue(str(post.updated.day) in response.content.decode('utf-8') or str(post.updated.day-1) in response.content.decode('utf-8')) # added this due to timezone issue
    # Check the link is marked up properly
		self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content.decode('utf-8'))
    # Check the correct template was used
		self.assertTemplateUsed(response, 'blog/jinja2/post.html')

	def test_category_page(self):
		post = PostFactory()
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)
		myPost = posts[0]
		self.assertEqual(myPost, post)
    # Get the category URL
		url = post.category.get_absolute_url()
    # Fetch the category
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
    # Check the category name is in the response
		self.assertTrue(post.category.name in response.content.decode('utf-8'))
    # Check the post text is in the response
		self.assertTrue(post.description in response.content.decode('utf-8'))
    # Check the post date is in the response
		self.assertTrue(str(post.updated.year) in response.content.decode('utf-8'))
		self.assertTrue(post.updated.strftime('%b') in response.content.decode('utf-8'))
		self.assertTrue(str(post.updated.day) in response.content.decode('utf-8') or str(post.updated.day-1) in response.content.decode('utf-8')) # added this due to timezone issue
    # Check the correct template was used
		self.assertTemplateUsed(response, 'blog/jinja2/category_view.html')

	def test_nonexistent_category_page(self):
		url = '/blog/category/blah/'
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue('No posts' in response.content.decode('utf-8'))

	def test_tag_page(self):
		author = AuthorFactory()
		site = SiteFactory()
		post = PostFactory()
		tag = TagFactory()
		post.tags.add(tag)
    # Check new post saved
		posts = Post.objects.all()
		self.assertEqual(len(posts), 1)
		myPost = posts[0]
		self.assertEqual(myPost, post)
    # Get the tag URL
		url = post.tags.all()[0].get_absolute_url()
    # Fetch the tag
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
    # Check the tag name is in the response
		self.assertTrue(post.tags.all()[0].name in response.content.decode('utf-8'))
    # Check the post text is in the response
		self.assertTrue(post.description in response.content.decode('utf-8'))
    # Check the post date is in the response
		self.assertTrue(str(post.updated.year) in response.content.decode('utf-8'))
		self.assertTrue(post.updated.strftime('%b') in response.content.decode('utf-8'))
		self.assertTrue(str(post.updated.day) in response.content.decode('utf-8') or str(post.updated.day-1) in response.content.decode('utf-8')) # added this due to timezone issue
    # Check the correct template was used
		self.assertTemplateUsed(response, 'blog/jinja2/tag_view.html')

	def test_nonexistent_tag_page(self):
		url = '/blog/tag/blah/'
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue('No posts' in response.content.decode('utf-8'))

    # def test_clear_cache(self):
    #     # Create the first post
    #     post = PostFactory(body='This is [my first blog post](http://127.0.0.1:8000/)')
    #     tag = TagFactory(name='perl', description='The Perl programming language')
    #     post.tags.add(tag)
	#
    #     # Check new post saved
    #     posts = Post.objects.all()
    #     self.assertEqual(len(posts), 1)
	#
    #     # Fetch the index
    #     response = self.client.get(reverse('blog:index'))
    #     self.assertEqual(response.status_code, 200)
	#
    #     # Create the second post
    #     post = PostFactory(title='My second post',body='This is [my second blog post](http://127.0.0.1:8000/)', slug='my-second-post')
    #     post.tags.add(tag)
	#
    #     # Fetch the index again
    #     response = self.client.get(reverse('blog:index'))
	#
    #     # Check second post present
	# 	self.assertTrue('my second blog post' in response.content.decode('utf-8'))

class FlatPageViewTest(BaseAcceptanceTest):
	def test_create_flat_page(self):
    # Create flat page
		page = FlatPageFactory(template_name='blog/flatpages/default.html')
    # Add the site
		page.sites.add(Site.objects.all()[0])
		page.save()
    # Check new page saved
		pages = FlatPage.objects.all()
		self.assertEqual(len(pages), 1)
		myPage = pages[0]
		self.assertEqual(myPage, page)
    # Check data correct
		self.assertEqual(myPage.url, '/about/')
		self.assertEqual(myPage.title, 'About me')
		self.assertEqual(myPage.content, 'All about me')
		#print ("\nThe myPage url is %s\n and the original page url is %s\n" % (myPage.url, page.url))
    # Get URL
		url = str(myPage.get_absolute_url())
    # Get the page
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
    # Check title and content in response
		self.assertTrue('About me' in response.content.decode('utf-8'))
		self.assertTrue('All about me' in response.content.decode('utf-8'))

class SearchViewTest(BaseAcceptanceTest):
	def test_search(self):
    # Create a post
		post = PostFactory()
    # Create another post
		post2 = PostFactory(body='This is my *second* blog post', title='My second post', slug='my-second-post')
    # Search for first post
		response = self.client.get(reverse('blog:search') + '?q=test')
		self.assertEqual(response.status_code, 200)
    # Check the first post is contained in the results
		self.assertTrue('Test Post' in response.content.decode('utf-8'))
    # Check the second post is not contained in the results
		self.assertTrue('My second post' not in response.content.decode('utf-8'))
    # Search for second post
		response = self.client.get(reverse('blog:search') + '?q=second')
		self.assertEqual(response.status_code, 200)
    # Check the first post is not contained in the results
		self.assertTrue('test post' not in response.content.decode('utf-8'))
    # Check the second post is contained in the results
		self.assertTrue('My second post' in response.content.decode('utf-8'))

	def test_failing_search(self):
    # Search for something that is not present
		response = self.client.get(reverse('blog:search') + '?q=wibble')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('No posts' in response.content.decode('utf-8'))
    # Try to get nonexistent second page
		response = self.client.get(reverse('blog:search') + '?q=wibble&page=2')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('No posts' in response.content.decode('utf-8'))

class SitemapTest(BaseAcceptanceTest):
	def test_sitemap(self):
    # Create a post
		post = PostFactory()
    # Create a flat page
		page = FlatPageFactory()
    # Get sitemap
		response = self.client.get('/sitemap.xml')
		self.assertEqual(response.status_code, 200)
    # Check post is present in sitemap
		self.assertTrue('test-post' in response.content.decode('utf-8'))
    # Check page is present in sitemap
		self.assertTrue('/about/' in response.content.decode('utf-8'))
