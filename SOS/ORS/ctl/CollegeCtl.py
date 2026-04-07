from multiprocessing.reduction import duplicate

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import College
from ..service.CollegeService import CollegeService

class CollegeCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['address'] = requestForm['address']
        self.form['state'] = requestForm['state']
        self.form['city'] = requestForm['city']
        self.form['phoneNumber'] = requestForm['phoneNumber']

    def form_to_model(self,obj):
        pk = int(self.form['id'])
        if pk>0:
            obj.id = pk
        obj.name = self.form['name']
        obj.address = self.form['address']
        obj.state = self.form['state']
        obj.city = self.form['city']
        obj.phoneNumber = self.form['phoneNumber']
        return obj

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['address'] = obj.address
        self.form['state'] = obj.state
        self.form['city'] = obj.city
        self.form['phoneNumber'] = obj.phoneNumber

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['name']):
            inputError['name'] = "College name cannot be null."
            self.form['error'] = True
        else:
            if DataValidator.isalphacheck(self.form['name']):
                inputError['name'] = "College name considers only letters"
                self.form['error'] = True
        if DataValidator.isNull(self.form['address']):
            inputError['address'] = "College address cannot be null."
            self.form['error'] = True
        if DataValidator.isNull(self.form['state']):
            inputError['state'] = "College state cannot be null."
            self.form['error'] = True
        if DataValidator.isNull(self.form['city']):
            inputError['city'] = "College city cannot be null."
            self.form['error'] = True
        if DataValidator.isNull(self.form['phoneNumber']):
            inputError['phoneNumber'] = "College phone number cannot be null."
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['phoneNumber'])):
                inputError['phonenNumber'] = "Only numbers allowed which start with 6,7,8,9."
                self.form['error'] = True
        return self.form['error']

    def display(self,request,params={}):
        if (params['id']>0):
            college = self.get_service().get(params['id'])
            self.model_to_form(college)
        res = render(request,self.get_template(),{"form":self.form})
        return res

    def submit(self, request, params={}):
        if (params['id']>0):
            pk = params['id']
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "College name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                college = self.form_to_model(College())
                self.get_service().save(college)
                self.form['id'] = college.id
                self.form['error'] = False
                self.form['message'] = "College updated successfully"
                res = render(request,self.get_template(),{"form":self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filtet(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "College name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                college = self.form_to_model(College())
                self.get_service().save(college)
                self.form['error'] = False
                self.form['message'] = "College saved successfully"
                res = render(request,self.get_template(),{"form":self.form})
            return res

    def get_service(self):
        return CollegeService()

    def get_template(self):
        return "College.html"
