from django.contrib import admin
from .models import Category, Author, Post, Comment, CategorySubscribers

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(CategorySubscribers)