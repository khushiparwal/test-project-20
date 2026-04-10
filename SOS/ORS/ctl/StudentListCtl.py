from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ..models import Student
from ..service.StudentService import StudentService

class StudentListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get('firstName', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        StudentListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Student.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        StudentListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = Student.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/Student/")
        return res

    def get_template(self):
        return "StudentList.html"

    def get_service(self):
        return StudentService()