from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from ..models import Role
from ..service.RoleService import RoleService


class RoleListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm['name']
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        RoleListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Role.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res


    def new(self, request, params={}):
        res = redirect("/ORS/Role/")
        return res

    def submit(self, request, params={}):
        RoleListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Role.objects.last().id
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "RoleList.html"

    def get_service(self):
        return RoleService()