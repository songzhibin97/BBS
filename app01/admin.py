from django.contrib import admin

# Register your models here.
from app01.models import UserInfo, Blog, Category, Tag, Article, ArticleDetail, Article2Tag, ArticleUpDown, Comment

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleDetail)
admin.site.register(Article2Tag)
admin.site.register(ArticleUpDown)
admin.site.register(Comment)
