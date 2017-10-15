from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

import logging

lista = []  # en forma de diccionario, almacenaré los eventos...

# logeamos
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Event\'s name', 'Date'], ['Priority', 'Something else...'], ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)


def facts_to_str(user_data):
    '''
    :param user_data: data from the user
    :return: espace + data [list-shape] + espace + espace
    '''

    facts = list()

    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    '''
    Shows a message and shows the markup keyboard
    :param bot: bot
    :param update: update
    :return: CHOOSING
    '''
    update.message.reply_text(
        "Hi! My name is ReminderHackUPC bot. I will remember importats facts for you :). "
        "Why don't you tell me something about yourself?",
        reply_markup = markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('Your %s? Yes, I would love to hear about that!' % text.lower())

    return TYPING_REPLY


def custom_choice(bot, update):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "%s"
                              "You can tell me more, or change your opinion on something."
                              % facts_to_str(user_data),
                              reply_markup = markup)

    return CHOOSING


def done(bot, update, user_data):
    '''
    :param bot: bot
    :param update: update
    :param user_data: we use 'facts_to_str' to give them shape
    :return: nothing. Finish the conversation and erase the data
    '''

    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("The event consists of:"
                              "%s"
                              "Don\'t forgot it!" % facts_to_str(user_data))
    # Si quiero guardar los datos es aquí dónde debo intervenir!!
    lista.append(facts_to_str(user_data))  # aquí mando ese diccionario a mi lista de pendientes
    almacenar(facts_to_str(user_data))     # almaceno los datos
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

## ===========================================================

def listado(bot, update):
    update.message.reply_text("The next events are:")
    for i in lista:
        update.message.reply_text("%s" % i)

def almacenar(data):
    file = open("Datos.txt", "a")
    file.write(data)
    flle.write('----------')
    file.close()

## ===========================================================

def main():
    TOKEN = '462467351:AAGf1qJTDN0xUik2NCY35YoWC3x9DyCBJm0'
    updater = Updater(TOKEN)

    # Obtenemos el  dispatcher para registrar los handlers
    dp = updater.dispatcher

    # Añadimos un Conversation handler con los estados GENDER, PHOTO, LOCATION y BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Event\'s name|Date|Priority)$',
                                    regular_choice,
                                    pass_user_data = True),
                       RegexHandler('^Something else...$',
                                    custom_choice),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data = True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data = True),
                           ],
        },

        fallbacks = [ RegexHandler('^Done$', done, pass_user_data = True) ]
    )

    dp.add_handler(conv_handler)

    ## ===========================================================

    dp.add_handler(CommandHandler("listado", listado))
    ## ===========================================================

    # logeamos los errores
    dp.add_error_handler(error)

    # Empezamos con el bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
