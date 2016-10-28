import datetime
import jinja2
import logging
import os
import traceback
import webapp2

from google.appengine.ext import ndb
from models import Student

jinja = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)

def render(template, values={}):
    return jinja.get_template(template).render(values)

def handler_404(request, response, exception):
    logging.exception(exception)
    response.write(render("templates/404.html"))
    response.set_status(404)

def handler_500(request, response, exception):
    logging.exception(exception)
    response.write(render("templates/500.html", {"stack_trace": traceback.format_exc().strip()}))
    response.set_status(500)

class ClassesHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "turmas",
        }
        self.response.write(render("templates/alunos.html", values))

class ClassHandler(webapp2.RequestHandler):
    def get(self, id):
        values = {
            "active": "turmas",
        }
        self.response.write(render("templates/aluno.html", values))

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "home",
        }
        self.response.write(render("templates/home.html", values))

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "configuracoes",
        }
        self.response.write(render("templates/configuracoes.html", values))

class StudentHandler(webapp2.RequestHandler):
    def get(self, id):
        values = {
            "active": "alunos",
        }

        if id:
            student = Student.get_by_id(long(id))
            values["student"] = student
            values["id"] = id

        self.response.write(render("templates/aluno.html", values))

    def post(self, id):
        student = Student.get_by_id(long(id)) if id else Student()
        student.populate(
            name=self.request.get("name"),
            surname=self.request.get("surname"),
            first_contact=datetime.datetime.strptime(self.request.get("first_contact"), "%d/%m/%Y").date(),
            telephone=self.request.get("telephone"),
            email=self.request.get("email"),
        )
        student.put()

        self.redirect("/aluno/" + str(student.key.id()))

    def delete(self, id):
        ndb.Key(Student, long(id)).delete()

class StudentsHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "alunos",
        }
        self.response.write(render("templates/alunos.html", values))

class TeacherHandler(webapp2.RequestHandler):
    def get(self, id):
        values = {
            "active": "professores",
        }
        self.response.write(render("templates/aluno.html", values))

class TeachersHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            "active": "professores",
        }
        self.response.write(render("templates/alunos.html", values))
