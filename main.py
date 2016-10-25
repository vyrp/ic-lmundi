import webapp2
from controllers import HomeHandler, handler_404

app = webapp2.WSGIApplication([
    ('/(?:home)?', HomeHandler),
], debug=True)

app.error_handlers[404] = handler_404
