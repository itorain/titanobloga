from django.contrib import admin
from .models import Post, Category, Tag

# Register the models
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title',)}
	list_filter = ('categories',)
	search_fields = ['title', 'description', 'content']
	
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class TagAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	
