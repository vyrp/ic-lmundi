import webapp2

from helpers import active, render
from models.settings import Settings


class HomeHandler(webapp2.RequestHandler):
    @active("home")
    def get(self, values):
        self.response.write(render("templates/home.html", values))


class SettingsHandler(webapp2.RequestHandler):
    @active("configuracoes")
    def get(self, values):
        settings = Settings.get_instance()
        for category in settings:
            values[category] = sorted(settings[category].values.items())
        self.response.write(render("templates/configuracoes.html", values))
