import json
import threading
import webapp2

from google.appengine.ext import ndb


class _SynchronizedDict():
    def __init__(self, json_dict):
        string_keys = json.loads(json_dict)
        self.values = {int(k): v for k, v in string_keys.iteritems()}
        self.lock = threading.Lock()
        self.counter = max(self.values.keys()) if self.values.keys() else 0

    def __repr__(self):
        return json.dumps(self.values)

    def add(self, value):
        """
        Returns the new id.
        """
        with self.lock:
            self.counter += 1
            self.values[self.counter] = value
            return self.counter

    def edit(self, id, new_value):
        """
        Returns True if the id was there, False otherwise.
        """
        with self.lock:
            if id in self.values:
                self.values[id] = new_value
                return True
            return False

    def remove(self, id):
        """
        Returns True if the id was there, False otherwise.
        """
        with self.lock:
            if id in self.values:
                del self.values[id]
                return True
            return False


class Settings(ndb.Model):
    emails = ndb.TextProperty(default="{}", required=True)
    languages = ndb.TextProperty(default="{}", required=True)
    modalities = ndb.TextProperty(default="{}", required=True)
    payments = ndb.TextProperty(default="{}", required=True)

    @classmethod
    def get_instance(cls):
        app = webapp2.get_app()
        with app.registry.get("settings_lock"):
            settings = app.registry.get("settings")
            if not settings:
                instance = cls.get_or_insert("instance")
                app.registry["settings"] = {
                    "emails": _SynchronizedDict(instance.emails),
                    "languages": _SynchronizedDict(instance.languages),
                    "modalities": _SynchronizedDict(instance.modalities),
                    "payments": _SynchronizedDict(instance.payments),
                }

            return app.registry["settings"]

    @classmethod
    def save(cls):
        app = webapp2.get_app()
        with app.registry.get("settings_lock"):
            instance = cls.get_by_id("instance")
            settings = app.registry.get("settings")
            instance.populate(
                emails=repr(settings["emails"]),
                languages=repr(settings["languages"]),
                modalities=repr(settings["modalities"]),
                payments=repr(settings["payments"]),
            )
            instance.put()
