import pickle

# data = ["a list", "containing", 5, 10, "abc", ["another", "list"]]
#
# with open("pickled list", 'wb') as fd:
#     pickle.dump(data, fd, protocol=1)
#
# with open("pickled list", 'rb') as fd:
#     loaded = pickle.load(fd)
#
# print(loaded)
# assert loaded == data
# print(id(data) == id(loaded))

from threading import Timer
from datetime import datetime
from urllib.request import urlopen


class UpdateURL:
    def __init__(self, url):
        self.url = url
        self.content = ""
        self.last_update = None
        self.update()
        self.timer = None

    def update(self):
        self.content = urlopen(self.url).read()
        self.last_update = datetime.now()
        self.schedule()

    def schedule(self):
        self.timer = Timer(3600, self.update)  # thread
        self.timer.setDaemon(True)
        self.timer.start()

    def __getstate__(self):
        new_state = self.__dict__.copy()
        if "timer" in new_state:
            del (new_state["timer"])
        return new_state

    def __setstate__(self, data):
        self.__dict__ = data
        self.schedule()


# serialize thread
# not normally picked objects: threads, sockets, file descriptor, DB connection
u = UpdateURL("http://news.yahoo.com")
serialized = pickle.dumps(u)  # return types object, not working for threads

# load/loads rebuild the object then calls __setstate__, the argument is the return value of __getstate__.
# can execute operations to rebuild not serializable objects here.
loaded = pickle.loads(serialized)


"""
pickle stores __dict__ attributes.
before that, store the return value of __getstate__ instead if available.
modify __getstate__ method to exclude not serializable attributes
"""
