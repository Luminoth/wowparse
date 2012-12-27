class PrefixFilter(object):
    def __init__(self, prefix):
        self.__prefix = prefix

    def filter(self, event):
        return event.prefix == self.__prefix
