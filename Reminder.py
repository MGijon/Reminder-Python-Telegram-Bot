from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

import logging


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
        "Hi! My name is ReminderHackUPC bot. I will remember importats facts for you :). ",
        reply_markup = markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('%s' % text.lower())

    return TYPING_REPLY


def custom_choice(bot, update):
    update.message.reply_text('Alright!!, something different', reply_markup = markup)

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you told me:"
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
    almacenar(facts_to_str(user_data))     # almaceno los datos
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

## ===========================================================

def listado(bot, update):
    update.message.reply_text("The next events are:")
    #chat_id = bot.get_updates()['id'].message.chat_id
    #bot.send_document(chat_id = chat_id, document = open('Datos.txt', 'rb'))
    file = open("Datos.txt", "r")
    cadena = ''
    for line in file.readlines():
        cadena += line
        cadena += '\n'
    update.message.reply_text("%s" % cadena)
    file.close()

def almacenar(data):
    file = open("Datos.txt", "a")
    file.write(data)
    file.write('----------')
    file.close()

## ===========================================================

def main():
    TOKEN = ''
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
