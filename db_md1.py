from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

url = ['/home/', '/admin/', '/Verification/', '/login/', '/enrol/', '/enrol/', '/logout/', '/media/']


class Log(MiddlewareMixin):
    def process_request(self, request):
        for u in url:
            if u in request.path_info:
                return
        return redirect("/home/")
