from django.shortcuts import render, redirect
from ..models import TimeTable
from .BaseCtl import BaseCtl
from ..service.TimeTableService import TimeTableService


class TimeTableListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['semester'] = requestForm.get('semester', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        TimeTableListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = TimeTable.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def submit(self, request, params={}):
        TimeTableListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = TimeTable.objects.last().id
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/TimeTable/")
        return res

    def get_template(self):
        return "TimeTableList.html"

    def get_service(self):
        return TimeTableService()