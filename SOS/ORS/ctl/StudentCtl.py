from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Student
from ..service.StudentService import StudentService

class StudentCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['dob'] = requestForm['dob']
        self.form['mobileNumber'] = requestForm['mobileNumber']
        self.form['email'] = requestForm['email']
        self.form['collegeId'] = requestForm['collegeId']
        self.form['collegeName'] = requestForm['collegeName']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.dob = self.form['dob']
        obj.mobileNumber = self.form['mobileNumber']
        obj.email = self.form['email']
        obj.collegeId = self.form['collegeId']
        obj.collegeName = self.form['collegeName']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "First Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['dob'])):
            inputError['dob'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['mobileNumber'])):
            inputError['mobileNumber'] = "Mobile Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobileNumber'])):
                inputError['mobileNumber'] = "Mobile Number must start with 6,7,8,9"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['email'])):
            inputError['email'] = "Email can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email Id must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['collegeId'])):
            inputError['collegeId'] = "College can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['collegeName'])):
            inputError['collegeName'] = "College Name can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.dynamic_preload})
        return res

    def submit(self, request, params={}):
        duplicate = self.get_service().get_model().objects.filter(email=self.form['email'])
        if duplicate.count() > 0:
            self.form['error'] = True
            self.form['message'] = "Email already exists"
            res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.dynamic_preload})
        else:
            student = self.form_to_model(Student())
            self.get_service().save(student)
            self.form['error'] = False
            self.form['message'] = "Student added successfully"
            res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.dynamic_preload})
        return res

    def get_template(self):
        return "Student.html"

    def get_service(self):
        return StudentService()