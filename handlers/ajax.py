import webapp2


class AjaxHandler(webapp2.RequestHandler):
    def post(self):
        self.response.write("All good!")
