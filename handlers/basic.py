import webapp2

from helpers import active, render


class HomeHandler(webapp2.RequestHandler):
    @active("home")
    def get(self, values):
        self.response.write(render("templates/home.html", values))


class SettingsHandler(webapp2.RequestHandler):
    @active("configuracoes")
    def get(self, values):
        self.response.write(render("templates/configuracoes.html", values))
