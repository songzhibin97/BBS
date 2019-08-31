"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls import include
from app01 import urls as app01_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', views.home),  # 首页
    # url(r'^Verification/', views.verification),  # 验证
    url(r'^login/', views.my_login),  # 登录
    url(r'^enrol/', views.enrol),  # 注册
    url(r'^logout/', views.my_logout),  # 注销
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),  # 配置上传图片存放的路由
    url(r'^article_media/', views.article_media),  # 处理创建博客上传图片的函数
    url(r'^bbs/', include(app01_urls)),  # 路由路由
    url(r'^praise/', views.praise),  # 登录
    url(r'^comment/', views.comment),  # 处理消息回复的函数
    # url(r'^comment_tree/', views.comment_tree),  # 处理消息回复的函数
    url(r'^create_article/', views.create_article),  # 处理创建文章函数
    url(r'^edit_article/', views.edit_article),  # 处理修改博客内容函数
    url(r'^delete_article/', views.delete_article),  # 处理删除博客内容函数
    url(r'^alter_article/', views.alter_article)  # 处理修改博客内容

]
