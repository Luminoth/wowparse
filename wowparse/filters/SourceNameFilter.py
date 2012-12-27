class SourceNameFilter(object):
    def __init__(self, name):
        self.__name = name

    def filter(self, event):
        return event.source_name == self.__name