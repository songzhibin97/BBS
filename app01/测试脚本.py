import os

if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BBS.settings")
    # 导入Django,并启动Django项目
    import django

    django.setup()
    # 已成功导入Django的环境可以使用Django的变量
    from app01 import models  # 导入app
    from django.db.models import Count
    from django.db.models import F

    # 进行操作
    user = models.UserInfo.objects.filter(username='bin')[0]
    blog = user.blog
    art = models.Article.objects.filter(user=user).values("aid")
    cat = models.Category.objects.filter(blog=blog).annotate(c=Count("article"))
    tag = models.Tag.objects.filter(blog=blog).annotate(c=Count('article'))
    user3 = models.UserInfo.objects.filter(username='bin').extra(
        select={"c": "date_format(create_time,'%%y-%%m')"}).annotate(con=Count('blog')).values("c", "con")
    # article = Article.objects.filter(user='bin')
    art_detail = models.Article.objects.all().values("articledetail__content")
    user_id = models.UserInfo.objects.filter(username='bin').values("uid").first()
    models.Comment.objects.filter(article_id=1).values("cid", "create_time", "parent_comment_id", "user__username",
                                                       'content')
    models.ArticleDetail.objects.filter(aid=9).first()
    ret = models.Article.objects.filter(aid=10)[0]

    print(ret.title)
