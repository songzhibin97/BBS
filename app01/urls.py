from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'(?P<username>.+)/(?P<page>.+)', views.blog_page),
    url(r'(?P<username>.+)', views.oneself),

]
