class DestNameFilter(object):
    def __init__(self, name):
        self.__name = name

    def filter(self, event):
        return event.dest_name == self.__name
