import webapp2

from helpers import render, secure


class ClassesHandler(webapp2.RequestHandler):
    @secure
    def get(self):
        values = {
            "active": "turmas",
        }
        self.response.write(render("templates/alunos.html", values))


class ClassHandler(webapp2.RequestHandler):
    @secure
    def get(self, id):
        values = {
            "active": "turmas",
        }
        self.response.write(render("templates/aluno.html", values))
