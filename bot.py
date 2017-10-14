import logging

logging.basicConfig(level = logging.DEBUG, format = )


TOKEN = '462467351:AAGf1qJTDN0xUik2NCY35YoWC3x9DyCBJm0'
bot = telebot.TeleBot(TOKEN)


user = bot.get_me()
print(user)

updates = bot.get_updates(1234,100,20) #get_Updates(offset, limit, timeout):#
#print([u.message.text for u in updates])


#chat_id = bot.get_updates()[-1].message.chat_id

# --------------------------------------------
# COMANDS:
# --------------------------------------------

## HELP



bot.polling()



# --------------------------------------------
# EVENT:
# --------------------------------------------


class evento(object):

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


