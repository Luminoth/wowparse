MATCH_TYPES = [ "None", "Any", "All" ]

class FilterConfig(object):
    MATCH_NONE = 0
    MATCH_ANY = 1
    MATCH_ALL = 2

    __config = {}
    __instantiated = False

    def __init__(self):
        self.__dict__ = self.__config

        if not self.__instantiated:
            self.__filters = []
            self.__match = FilterConfig.MATCH_ANY

        self.__instantiated = True

    @property
    def filters(self):
        return self.__filters

    @property
    def filter_count(self):
        return len(self.__filters)

    @property
    def match(self):
        return self.__match

    def clear(self):
        self.__filters = []

    def add_filter(self, filter):
        self.__filters.append(filter)

    def remove_filter(self, idx):
        del self.__filters[idx]

    def filter(self, event):
        if self.filter_count == 0:
            return True

        if self.match == FilterConfig.MATCH_NONE:
            for filter in self.filters:
                if filter.filter(event):
                    return False
            return True
        elif self.match == FilterConfig.MATCH_ANY:
            for filter in self.filters:
                if filter.filter(event):
                    return True
            return False
        elif self.match == FilterConfig.MATCH_ALL:
            for filter in self.filters:
                if not filter.filter(event):
                    return False
            return True

        return filters.filter_count == 0
