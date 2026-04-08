from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Course
from ..service.CourseService import CourseService

class CourseCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['description'] = requestForm['description']
        self.form['duration'] = requestForm['duration']

    def form_to_model(self,obj):
        pk = int(self.form['id'])
        if pk>0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.duration = self.form['duration']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Course name cannot be null."
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Course name contains only letters"
                self.form['error'] = True
        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Course Description cannot be null."
            self.form['error'] = True
        if (DataValidator.isNull(self.form['duration'])):
            inputError['duration'] = "Course Duration cannot be null"
            self.form['error'] = True
        return self.form['error']

    def display(self,request,params={}):
        res = render(request,self.get_template(),{"form":self.form})
        return res

    def submit(self, request, params={}):
        duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
        if duplicate.count() > 0:
            self.form['error'] = True
            self.form['message'] = "Course name already exists"
            res = render(request,self.get_template(),{"form":self.form})
        else:
            course = self.form_to_model(Course())
            self.get_service().save(course)
            self.form['error']=False
            self.form['message'] = "Course added successfully"
            res = render(request,self.get_template(),{"form":self.form})
        return res

    def get_template(self):
        return "Course.html"

    def get_service(self):
        return CourseService()
