class Contact:
    def __init__(self, first, last):
        self._first = first
        self._last = last

    @property  # beans: getter, setter, deleter
    def full_name(self):
        return "{} {}".format(self._first, self._last)

    @full_name.setter
    def full_name(self, fullname):
        name = fullname.split()
        self._first = name[0]
        self._last = name[1]

    @full_name.deleter
    def full_name(self):
        del self._first
        del self._last


import json

c = Contact("John", "Smith")


# json.dumps(c.__dict__)

class ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Contact):
            return {'is_contact': True,
                    'full': obj.full_name}
        return super().default(obj)


jsoned = json.dumps(c, cls=ContactEncoder)


def decode_contact(dic):
    if dic["is_contact"]:
        fname = dic["full"].split()
        contact = Contact(fname[0], fname[1])
        return contact
    else:
        return dic


rebuilt = json.loads(jsoned, object_hook=decode_contact)
print(type(rebuilt), rebuilt.full_name)
