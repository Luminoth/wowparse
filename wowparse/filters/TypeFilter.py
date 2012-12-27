class TypeFilter(object):
    def __init__(self, type):
        self.__type = type

    def filter(self, event):
        return event.type_name == self.__type
