import statuses
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

    def strictly_positive(self, value):
        if value > 0:
            return value
        raise ValueError("Index must be > 0.")

    # Indexed because search
    first_contact = ndb.DateProperty(validator=recent_date)
    language_ids_interested = ndb.IntegerProperty(repeated=True, validator=strictly_positive)
    status = ndb.IntegerProperty(choices=set(range(1, statuses.END)), default=0)

    # Indexed because sort
    name = ndb.StringProperty(required=True, validator=non_empty)
    surname = ndb.StringProperty(validator=non_empty)
    email = ndb.StringProperty(validator=non_empty)

    # Indexed because projection
    telephones = ndb.StringProperty(repeated=True, validator=validate_telephone)  # required

    # Not indexed
    modality_ids_interested = ndb.IntegerProperty(
        indexed=False, repeated=True, validator=strictly_positive)
    made_lvl_test = ndb.BooleanProperty(default=False, indexed=False)
    lvl = ndb.StringProperty(indexed=False)
    turma = ndb.IntegerProperty(indexed=False, validator=strictly_positive)
    available_times = ndb.StringProperty(indexed=False)
    obs = ndb.TextProperty()
    extra_info = ndb.TextProperty()
