from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

url = ['/home/', '/admin/', '/Verification/', '/edit_article/', 'delete_article',
       '/login/', '/enrol/', '/bbs/', 'praise/', '/comment/', '/alter_article/',
       '/logout/', '/media/', '/comment_tree/',
       '/create_article/', '/article_media/']


class Log(MiddlewareMixin):
    def process_request(self, request):
        for u in url:
            if u in request.path_info:
                return
        return redirect("/home/")
