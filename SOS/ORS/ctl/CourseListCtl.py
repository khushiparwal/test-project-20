from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ..models import Course
from ..service.CourseService import CourseService

class CourseListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get('name',None)
        self.form['ids'] = requestForm.getlist('ids',None)

    def display(self,request,params={}):
        CourseListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Course.objects.last().id
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def new(self,request, params={}):
        res = redirect("/ORS/Course/")
        return res

    def submit(self, request, params={}):
        CourseListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Course.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "CourseList.html"

    def get_service(self):
        return CourseService()