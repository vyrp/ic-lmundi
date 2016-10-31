import webapp2

from helpers import render


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
