import markdown
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    """
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    # Meta自定义一些元数据信息，例如修改Django命令自动生成的表名
    class Meta:
        # verbose_name 用于显示在管理后台中的名称
        verbose_name = '种类'

        # verbose_name_plural 表示显示在管理后台名称中的复数
        verbose_name_plural = verbose_name

    # __str__函数用于 自定义print实例对象时的输出内容
    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签类
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章类
    """

    # 文章标题
    title = models.CharField('标题', max_length=70)

    # 文章正文
    # 存储比较短的字符可以用CharField，存储文章的正文可能是大段文本，同TextField 来存储大段文本
    body = models.TextField('正文')

    # 创建时间和最后修改时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要，文章可以没有，单默认情况下 CharField 要求我们必须存入数据，否则就会报错
    # 指定 CharField 的 blank=True参数值后就可以允许空值了
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和Category 类似。
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

        # 指定返回的文章列表的顺序
        # 可以有多个选项，例如ordering = ['-created_time', 'title']，根据时间进行排序，若时间相同，再根据title进行排序
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # *args 用来将参数打包成tuple给函数体调用  **kwargs 打包关键字参数成dict给函数体调用

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 摘要实现
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
