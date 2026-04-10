from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ..utility.DataValidator import DataValidator
from ..models import College
from ..service.CollegeService import CollegeService

class CollegeListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get("name",None)
        self.form['ids'] = requestForm.getlist('ids',None)

    def display(self,request,params={}):
        CollegeListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = College.objects.last().id
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def new(self,request, params={}):
        res = redirect("/ORS/College")
        return res

    def submit(self, request, params={}):
        CollegeListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "CollegeList.html"

    def get_service(self):
        return CollegeService()