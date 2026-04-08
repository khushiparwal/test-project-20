from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from ..models import TimeTable
from ..service.TimeTableService import TimeTableService

class TimeTableCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['examTime'] = requestForm['examTime']
        self.form['examDate'] = requestForm['examDate']
        self.form['courseId'] = requestForm['courseId']
        self.form['courseName'] = requestForm['courseName']
        self.form['subjectId'] = requestForm['subjectId']
        self.form['subjectName'] = requestForm['subjectName']
        self.form['semester'] = requestForm['semester']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.examTime = self.form['examTime']
        obj.examDate = self.form['examDate']
        obj.courseId = self.form['courseId']
        obj.courseName = self.form['courseName']
        obj.subjectId = self.form['subjectId']
        obj.subjectName = self.form['subjectName']
        obj.semester = self.form['semester']
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['examTime'])):
            inputError['examTime'] = "Exam Time can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['examDate'])):
            inputError['examDate'] = "Exam Date can not be null"
            self.form['error'] = True

        if (DataValidator.isNotNull(self.form['examDate'])):
            if (DataValidator.isDate(self.form['examDate'])):
                inputError['examDate'] = "Incorrect date format, should be YYYY-MM-DD"
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

        if (DataValidator.isNull(self.form['subjectId'])):
            inputError['subjectId'] = "Subject can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['semester'])):
            inputError['semester'] = "Semester can not be null"
            self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        duplicate = TimeTable.objects.filter(
            subjectId=self.form['subjectId'],
            examTime=self.form['examTime'],
            examDate=self.form['examDate']
        )
        if duplicate.count() > 0:
            self.form['error'] = True
            self.form['message'] = "Exam Time, Exam Date, Subject name already exists"
            return render(request, self.get_template(), {
                    'form': self.form})
        else:
            timeTable = self.form_to_model(TimeTable())
            self.get_service().save(timeTable)
            self.form['error'] = False
            self.form['message'] = "Timetable added successfully"
            return render(request, self.get_template(), {
                    'form': self.form})

    def get_template(self):
        return "TimeTable.html"

    def get_service(self):
        return TimeTableService()