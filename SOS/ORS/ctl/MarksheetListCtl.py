from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ..models import Marksheet
from ..service.MarksheetService import MarksheetService


class MarksheetListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["rollNumber"] = requestForm.get("rollNumber", None)
        self.form["ids"] = requestForm.getlist("ids", None)

    def display(self, request, params={}):
        MarksheetListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form['lastId'] = Marksheet.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        MarksheetListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form['lastId'] = Marksheet.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list, 'form': self.form})
        return res

    def new(self, request, params={}):
        res = redirect("/ORS/Marksheet/")
        return res

    def get_template(self):
        return "MarksheetList.html"

    def get_service(self):
        return MarksheetService()