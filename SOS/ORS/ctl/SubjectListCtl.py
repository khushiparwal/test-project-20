from django.shortcuts import render, redirect
from ..models import Subject
from .BaseCtl import BaseCtl
from ..service.SubjectService import SubjectService


class SubjectListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get('name', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        SubjectListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Subject.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def submit(self, request, params={}):
        SubjectListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Subject.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res


    def new(self, request, params={}):
        res = redirect("/ORS/Subject/")
        return res

    def get_template(self):
        return "SubjectList.html"

    def get_service(self):
        return SubjectService()