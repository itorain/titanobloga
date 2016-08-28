from django.contrib import admin
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	exclude = ('author',)
	list_filter = ('categories',)
	search_fields = ['title', 'description', 'content']
		
	def save_model(self, request, obj, form, change):
		obj.author = request.user
		obj.save()
	
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	
# Register the models
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
