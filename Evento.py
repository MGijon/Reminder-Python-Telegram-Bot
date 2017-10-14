class Evento(object):

    ''' CLASS EVENT:

    Parameters:
        name : name of the event to remind
        date : date of the event to remind
        priority : priority of the event to remind

    '''

    def __init__(self, date, priority, name):
        self.name = name
        self.date = date
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del _name

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @date.deleter
    def date(self):
        del self._date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self.name


