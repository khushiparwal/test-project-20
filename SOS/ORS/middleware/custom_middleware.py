from django.http import HttpResponse
from django.shortcuts import render,redirect

class FrontCtlMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path_info in ['/','/ORS/Login/','/ORS/Welcome/','/ORS/Registration/','/ORS/Logout/','/ORS/ForgetPassword/']:
            return self.get_response(request)
        if  not request.session.get('user'):
            message = "Session expired. Please login again."
            return render(request,'Login.html',{'message':message})
        return self.get_response(request)