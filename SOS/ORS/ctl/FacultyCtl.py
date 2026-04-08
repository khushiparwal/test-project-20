from django.shortcuts import render
from .BaseCtl import BaseCtl
from ..service.FacultyService import FacultyService
from ..utility.DataValidator import DataValidator
from ..models import Faculty

class FacultyCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['email'] = requestForm['email']
        self.form['password'] = requestForm['password']
        self.form['address'] = requestForm['address']
        self.form['gender'] = requestForm['gender']
        self.form['dob'] = requestForm['dob']
        self.form['collegeId'] = requestForm['collegeId']
        self.form['collegeName'] = requestForm['collegeName']
        self.form['subjectId'] = requestForm['subjectId']
        self.form['subjectName'] = requestForm['subjectName']
        self.form['courseId'] = requestForm['courseId']
        self.form['courseName'] = requestForm['courseName']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.email = self.form['email']
        obj.password = self.form['password']
        obj.address = self.form['address']
        obj.dob = self.form['dob']
        obj.gender = self.form['gender']
        obj.collegeId = self.form['collegeId']
        obj.collegeName = self.form['collegeName']
        obj.subjectId = self.form['subjectId']
        obj.subjectName = self.form['subjectName']
        obj.courseId = self.form['courseId']
        obj.courseName = self.form['courseName']
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

        if (DataValidator.isNull(self.form['email'])):
            inputError['email'] = "Email can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            inputError['password'] = "password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['address'])):
            inputError['address'] = "Address can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['dob'])):
            inputError['dob'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseName'])):
            inputError['courseName'] = "Course name can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['subjectName'])):
            inputError['subjectName'] = "Subject name can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['collegeName'])):
            inputError['collegeName'] = "College name can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['collegeId'])):
            inputError['collegeId'] = "College can not be null"
            self.form['error'] = True


        if (DataValidator.isNull(self.form['subjectId'])):
            inputError['subjectId'] = "Subject can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        duplicate = self.get_service().get_model().objects.filter(email=self.form['email'])
        if (duplicate.count() > 0):
            self.form['error'] = True
            self.form['message'] = "Email already exists"
            res = render(request, self.get_template(), {'form': self.form})
        else:
            faculty = self.form_to_model(Faculty())
            self.get_service().save(faculty)
            self.form['error'] = False
            self.form['message'] = "Faculty added successfully"
            res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "Faculty.html"

    def get_service(self):
        return FacultyService()


