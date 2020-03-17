from django.db import models
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

    class Meta:
        # verbose_name 用于显示在管理后台中的名称
        verbose_name = '评论'

        # verbose_name_plural 表示显示在管理后台名称中的复数
        verbose_name_plural = verbose_name

        ordering = ['created_time']
