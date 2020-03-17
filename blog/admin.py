from django.contrib import admin
from .models import Post, Category, Tag


# 定制后台管理界面中的文章，让它不只显示标题，显示更多信息

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

    # 定制新增文章、修改文章页面所需填写的字段
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

