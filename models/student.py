import re

from google.appengine.ext import ndb


class Student(ndb.Model):
    _telephone_regex = re.compile(r"\(\d{2}\) \d{4,5}\-\d{4}$")

    def validate_telephone(self, value):
        value = value.strip()
        if Student._telephone_regex.match(value):
            return value
        raise ValueError(
            "Value '%s' doesn't match telephone regex '%s'."
            % (value, Student._telephone_regex.pattern)
        )

    def non_empty(self, value):
        value = value.strip()
        if value:
            return value
        raise ValueError("Value for '%s' is empty." % self._name)

    def recent_date(self, value):
        if value.year >= 1900:
            return value
        raise ValueError("Year must be >= 1900.")

    name = ndb.StringProperty(required=True, validator=non_empty)
    surname = ndb.StringProperty(required=True, validator=non_empty)
    first_contact = ndb.DateProperty(required=True, validator=recent_date)
    telephone = ndb.StringProperty(required=True, validator=validate_telephone)
    email = ndb.StringProperty(required=True, validator=non_empty)
