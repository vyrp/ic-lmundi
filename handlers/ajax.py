import webapp2

from models.settings import Settings


class AjaxHandler(webapp2.RequestHandler):
    def post(self, category, command):
        settings = Settings.get_instance()
        items = settings[category]

        if command == "add":
            value = self.must_get("value")
            new_id = items.add(value)
            self.response.write(str(new_id))

        elif command == "edit":
            id = int(self.must_get("id"))
            value = self.must_get("value")
            success = items.edit(id, value)
            if success:
                self.response.write("OK")
            else:
                self.abort(400, "ID %d doesn't exist." % id)

        elif command == "remove":
            id = int(self.must_get("id"))
            success = items.remove(id)
            if success:
                self.response.write("OK")
            else:
                self.abort(400, "ID %d doesn't exist." % id)

        else:
            self.abort(500, "Invalid command. Should not occur.")

        Settings.save()

    def must_get(self, field_name):
        field = self.request.get(field_name)
        if not field:
            self.abort(400, "Missing field '%s'." % field_name)
        return field
