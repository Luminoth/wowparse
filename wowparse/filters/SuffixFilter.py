class SuffixFilter(object):
    def __init__(self, suffix):
        self.__suffix = suffix

    def filter(self, event):
        return event.suffix == self.__suffix
