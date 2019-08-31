from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.models import UserInfo, Article, Blog, Category, Tag, ArticleDetail, ArticleUpDown, Comment
from .app01_form import Login, Enrol  # 引入form创建的类
# # 引入极验工具
# from geetest import GeetestLib
# 引入Django自带的验证工具 authenticate 验证是否登录 login 如果登录成功绑定用户信息在request中 logout 清除已经登录的信息
from django.contrib.auth import authenticate, login, logout
import json
# 引入Django自带的验证是否登录的装饰器
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F


# Create your views here.


# 处理首页函数
def home(request):
    article_obj = Article.objects.all()
    return render(request, "home.html", {"article_obj": article_obj})


# 处理登录函数
def my_login(request):
    if request.method == "POST":
        form_obj = Login(request.POST)
        # gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        # challenge = request.POST.get(gt.FN_CHALLENGE, '')
        # validate = request.POST.get(gt.FN_VALIDATE, '')
        # seccode = request.POST.get(gt.FN_SECCODE, '')
        # status = request.session[gt.GT_STATUS_SESSION_KEY]
        # user_id = request.session["user_id"]
        # if status:
        #     result = gt.success_validate(challenge, validate, seccode, user_id)
        # else:
        #     result = gt.failback_validate(challenge, validate, seccode)
        # if result:
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            password = form_obj.cleaned_data.get("password")
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)  # 如果登录成功绑定信息
                dat = {"mode": 1, "data": "登录成功"}
                data = json.dumps(dat)
                return HttpResponse(data)
            dat = {"mode": 0, "data": "账号或密码错误"}
            data = json.dumps(dat)
            return HttpResponse(data)
        dat = {"mode": 2, "errors": form_obj.errors}
        data = json.dumps(dat)
        return HttpResponse(data)

    form_obj = Login()
    return render(request, 'login.html', {"form_obj": form_obj})


# 处理注销函数
def my_logout(request):
    logout(request)
    return redirect('/home/')


# 处理注册函数
def enrol(request):
    if request.method == 'POST':
        form_obj = Enrol(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            password = form_obj.cleaned_data.get("password")
            avatar = request.FILES.get("avatar")
            try:
                UserInfo.objects.create_user(username=username, password=password, avatar=avatar)
                dat = {"mode": 1, "data": "注册成功"}
                data = json.dumps(dat)
                return HttpResponse(data)
            except Exception as e:
                dat = {"mode": 0, "data": "注册失败"}
                data = json.dumps(dat)
                return HttpResponse(data)
        dat = {"mode": 2, "errors": form_obj.errors}
        data = json.dumps(dat)
        return HttpResponse(data)

    form_obj = Enrol()
    return render(request, 'enrol.html', {"form_obj": form_obj})


# 极验验证码key value
# pc_geetest_id = "da84be6f2598a542d862bf40022a10b7"
# pc_geetest_key = "7db916b1736ff14a64efcb2f6a9c9101"
# pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
# pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
#
#
# def verification(request): # 获取极验验证码
#     user_id = 'test'
#     gt = GeetestLib(pc_geetest_id, pc_geetest_key)
#     status = gt.pre_process(user_id)
#     request.session[gt.GT_STATUS_SESSION_KEY] = status
#     request.session["user_id"] = user_id
#     response_str = gt.get_response_str()
#     return HttpResponse(response_str)


# 处理个人博客页面
@login_required  # Django内置校验登录装饰器 如果校验不成功则返回登录在settings配置 LOGIN_URL=url返回路径
def oneself(request, username):
    user_obj = UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    # 博客分类obj
    category = Category.objects.filter(blog=blog).annotate(c=Count("article"))
    # 标签分类obj
    tag = Tag.objects.filter(blog=blog).annotate(c=Count("article"))
    # 时间分类obj
    date = UserInfo.objects.filter(username=username).extra(
        select={"c": "date_format(create_time,'%%y-%%m')"}).annotate(con=Count("blog")).values("c", "con")
    # 文章内容
    article = Article.objects.filter(user=user_obj)
    return render(request, 'onself.html', {"user_obj": user_obj,
                                           "article": article,
                                           "category": category,
                                           "tag": tag,
                                           "date": date
                                           })


# 处理文章详情
def blog_page(request, username, page):
    # 找到博主
    user_obj = UserInfo.objects.filter(username=username).first()
    # 博主的博客
    blog = user_obj.blog
    # 博主博客分类obj
    category = Category.objects.filter(blog=blog).annotate(c=Count("article"))
    # 博主标签分类obj
    tag = Tag.objects.filter(blog=blog).annotate(c=Count("article"))
    # 博主时间分类obj
    date = UserInfo.objects.filter(username=username).extra(
        select={"c": "date_format(create_time,'%%y-%%m')"}).annotate(con=Count("blog")).values("c", "con")
    # 找到文章详情
    articledetail = ArticleDetail.objects.filter(aid=page).first()
    comment = Comment.objects.filter(article_id=articledetail.article_id)
    return render(request, 'blog_detail.html', {"articledetail": articledetail,
                                                "user_obj": user_obj,
                                                "category": category,
                                                "tag": tag,
                                                "date": date,
                                                "comment": comment
                                                })


# 处理文章点赞踩函数_ajax
def praise(request):
    username = json.loads(request.POST.get("user"))  # 获取点赞用户
    art = json.loads(request.POST.get("art"))  # 获取点赞文章
    praise = json.loads(request.POST.get("praise"))  # 获取是赞还是踩
    data = {"state": 0}  # 状态信息
    try:
        user_id = UserInfo.objects.filter(username=username).values("uid").first()["uid"]
        ArticleUpDown.objects.create(user_id=user_id, article_id=art, is_up=praise)
        data["state"] = 1  # 点赞或踩成功
        if praise:
            Article.objects.filter(aid=art).update(up_count=F('up_count') + 1)
            data["updown"] = True
        else:
            Article.objects.filter(aid=art).update(down_count=F('down_count') + 1)
    except Exception as e:
        data["state"] = 2  # 点赞或登录失败
        ret = ArticleUpDown.objects.filter(user_id=user_id, article_id=art).values("is_up").first()["is_up"]
        data['clue'] = ret
    return JsonResponse(data)


# 处理回复的函数_ajax
def comment(request):
    # 父评论ID 如果为根评论 sub_comment为0
    sub_comment = json.loads(request.POST.get("sub_comment"))
    # 评论文章ID
    comment_id = json.loads(request.POST.get("comment_id"))
    # 评论人ID
    user_id = json.loads(request.POST.get('user_id'))
    # 评论的内容
    content = request.POST.get('content')
    data = {}
    if sub_comment == 0:
        # 创建根评论
        try:
            Comment.objects.create(article_id=comment_id, user_id=user_id, content=content)
            data["state"] = 0  # 0 评论表示创建成功
            Article.objects.filter(aid=comment_id).update(comment_count=F('comment_count') + 1)
            return JsonResponse(data)
        except Exception as e:
            data["state"] = 1  # 1 表示创建失败
            return JsonResponse(data)

    else:
        # 创建子评论
        try:
            Comment.objects.create(article_id=comment_id, user_id=user_id, content=content,
                                   parent_comment_id=sub_comment)
            Article.objects.filter(aid=comment_id).update(comment_count=F('comment_count') + 1)
            data["state"] = 0  # 0 评论表示创建成功
            return JsonResponse(data)
        except Exception as e:
            data["state"] = 1
            return JsonResponse(data)


# # 处理评论树的函数_ajax
# def comment_tree(request):
#     article_id = request.POST.get("article_id")
#     ret = list(
#         Comment.objects.filter(article_id=article_id).values("cid", "create_time", "parent_comment_id",
#                                                              "user__username", 'content'))
#
#     return JsonResponse(ret, safe=False)


# 处理创建文章的函数
@login_required
def create_article(request):
    if request.method == "POST":
        import bs4
        title = request.POST.get("article_title")
        content = request.POST.get("article_content")
        content1 = bs4.BeautifulSoup(content, 'html.parser')
        for con in content1.find_all():
            if con.name in ["script", 'link']:
                con.decompose()
        user = request.user.uid
        filtrate_content = content1.text[:180] + '...'
        try:
            article_obj = Article.objects.create(title=title, desc=filtrate_content, user_id=user)
            detail_obj = ArticleDetail.objects.create(article_id=article_obj.aid, content=str(content1))
            return render(request, "reply.html", {"success_fail": "发表成功"})
        except Exception as e:
            return render(request, "reply.html", {"success_fail": "发表失败"})
    return render(request, 'create_article.html')


# 处理创建文章上传图片的函数
@login_required
def article_media(request):
    from BBS import settings
    import os
    import json
    img = request.FILES.get("new_image")
    path = os.path.join(settings.MEDIA_ROOT, "file_photo", img.name)
    with open(path, 'wb') as f:
        for i in img:
            f.write(i)
    ret = {
        "error": 0,  # 返回错误信息
        "url": "/media/file_photo/" + img.name  # 返回能访问到图片的路径
    }
    return HttpResponse(json.dumps(ret))


# 处理修改博客的函数
@login_required
def edit_article(request):
    edit_article_id = json.loads(request.POST.get('edit_article_id'))
    article_user_id = Article.objects.filter(aid=edit_article_id).values("user_id")[0]["user_id"]
    if article_user_id == request.user.uid:
        alter_article = Article.objects.filter(aid=edit_article_id).first()
        alter_articledetail_id = Article.objects.filter(aid=edit_article_id).values("articledetail__aid")[0][
            "articledetail__aid"]
        alter_articledetail = ArticleDetail.objects.filter(aid=alter_articledetail_id).first()
        return render(request, "alter_article.html",
                      {"alter_articledetail": alter_articledetail, 'alter_article': alter_article})


# 处理删除博客的函数
@login_required
def delete_article(request):
    delete_article_id = json.loads(request.POST.get("delete_article_id"))
    article_user_id = Article.objects.filter(aid=delete_article_id).values("user_id")[0]["user_id"]
    data = {}
    if article_user_id == request.user.uid:
        try:
            Article.objects.filter(aid=delete_article_id).delete()
            ArticleDetail.objects.filter(article_id=delete_article_id).delete()
            data["state"] = 0  # 状态码 0 为成功
            return JsonResponse(data)
        except Exception as e:
            data["state"] = 1
            return JsonResponse(data)
    else:
        data["state"] = 1


# 处理修改博客内容
@login_required
def alter_article(request):
    import bs4
    article_id = request.POST.get("article_id")
    articledetail_id = request.POST.get("articledetail_id")
    title = request.POST.get("article_title")
    content = request.POST.get("article_content")
    content1 = bs4.BeautifulSoup(content, 'html.parser')
    for con in content1.find_all():
        if con.name in ["script", 'link']:
            con.decompose()
    user = request.user.uid
    filtrate_content = bs4.BeautifulSoup(content, "html.parser").text[:180] + '...'
    try:

        new_article = Article.objects.filter(aid=article_id).update(title=title, desc=filtrate_content)
        new_detail = ArticleDetail.objects.filter(aid=articledetail_id).update(content=str(content1))
        return render(request, "reply.html", {"success_fail": "修改成功"})
    except Exception as e:
        return render(request, "reply.html", {"success_fail": "修改失败"})
