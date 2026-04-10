from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ..models import Faculty
from ..service.FacultyService import FacultyService

class FacultyListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get('firstName',None)
        self.form['ids'] = requestForm.getlist('ids',None)

    def display(self,request,params={}):
        FacultyListCtl.count = self.form['pageNo']
        record= self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Faculty.objects.last().id
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def new(self,request,params={}):
        res = redirect("/ORS/Faculty/")
        return res

    def submit(self, request, params={}):
        FacultyListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Faculty.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "FacultyList.html"

    def get_service(self):
        return FacultyService()