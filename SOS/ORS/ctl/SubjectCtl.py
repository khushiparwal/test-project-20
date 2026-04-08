from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from ..models import Subject
from ..service.SubjectService import SubjectService

class SubjectCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['description'] = requestForm['description']
        self.form['courseId'] = requestForm['courseId']
        self.form["courseName"] = requestForm['courseName']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.courseId = self.form['courseId']
        obj.courseName = self.form['courseName']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Subject Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Subject Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseName'])):
            inputError['courseName'] = "Course Name can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        return res

    def submit(self, request, params={}):
        duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
        if duplicate.count() > 0:
            self.form['error'] = True
            self.form['message'] = "Subject Name already exists"
            res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        else:
            subject = self.form_to_model(Subject())
            self.get_service().save(subject)
            self.form['error'] = False
            self.form['message'] = "Subject added successfully"
            res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        return res

    def get_template(self):
        return "Subject.html"

    def get_service(self):
        return SubjectService()