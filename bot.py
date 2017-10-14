from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

import collections


TOKEN = '462467351:AAGf1qJTDN0xUik2NCY35YoWC3x9DyCBJm0'

EVENT, NAME, DATA, PRIORITY = range(4)

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(name)s', level = logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command headlers. Usually take two arguments: bot and update.
# Error handlers also recive the raised TelegramError object in error.

def start(bot, update):
    update.message.reply_text('please, talk to me')

def help(bot, update):
    update.message.reply_text('Do you need help?.. poor boy')

def echo(bot, update):
    update.message.reply_text(update.message.text)

def error(bor, update, error):
    logger.warn('Update "%s" caused error "%s"' %(update, error))

def cancel(bot, updapte):
    user = update.message.from_user
    logger.info('You have canceled the event creation')
    update.message.reply_text('Hope see you soon')
    return ConversationHandler.EN

## .........................

def event(bot, update):

    keyboard = [[InlineKeyboardButton("Ok", callback_data = '1'), InlineKeyboardButton("Cancell", callback_data = '2')]]
    reply_markup = InlineKeyboardMarkup(keyboard) # create an 'array' with the bottons
    update.message.reply_text('Please, confirm that your want to create a new event:', reply_markup = reply_markup)


def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text = 'select option %s' % query.data, chat_id = query.message.chat_id, message_id = query.message.message_id )
    # now we return true to know if we have to continue with the flow of the program

def name(bot, update):
    update.message.reply_text('tell me how to name te event:')
    user = update.message.from_user
    NAME = update.message.text
    update.message.reply_text('Ok!', reply_markup = NAME)

    return NAME

def priority(bot, update):
    keyboard = [[InlineKeyboardButton(text = "low", callback_data = '3' ), InlineKeyboardButton(text = 'moderate', callback_data = 4)], [InlineKeyboardButton(text = 'high', callback_data = 5,), InlineKeyboardButton(text = 'super high', callback_data = 6)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select the priority of your event', reply_markup = reply_markup)

def buttonPriority(bot, update):
    query = update.callback_query
    bot.edit_message_text(text = 'select option %s' % query.data, chat_id = query.message.chat_id, message_id = query.message.message_id )

    PRIORITY = query.data

    return PRIORITY

def data(bot, update):
    # arreglar fuertemente
    keyboard = [
        [InlineKeyboardButton(text="low", callback_data='3'), InlineKeyboardButton(text='moderate', callback_data=4)],
        [InlineKeyboardButton(text='high', callback_data=5, ),
         InlineKeyboardButton(text='super high', callback_data=6)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select the priority of your event', reply_markup=reply_markup)

    DATA = reply_markup

    return DATA


def main():

    # Create and EventHandler and pass it yout bot's token
    updater = Updater(TOKEN)

    Evento = collections.namedtuple('evento', 'name date priority')  # creates de Evento class
    Eventos = []

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # ------------------------
    conv_Handler = ConversationHandler(
        entry_points = [CommandHandler("event", event), CommandHandler("name", name),  CommandHandler("data", data), CommandHandler("priority", priority)],
        states = {
            EVENT: [MessageHandler(Filters.text, event)],
            NAME: [MessageHandler(Filters.text, name)],
            DATA: [MessageHandler(Filters.text, data)],
            PRIORITY: [MessageHandler(Filters.text, priority)],
        },

        fallbacks = [CommandHandler('cancel', cancel)]

    )

    dp.add_handler(conv_Handler)

    # On differents commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))


    dp.add_handler(CommandHandler("event", event))
    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(CommandHandler("name", name))

    dp.add_handler(CommandHandler("priority", priority))
    dp.add_handler(CallbackQueryHandler(buttonPriority))

    # On noncommand i.e. message - echo the messageon Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Log all the errors
    dp.add_error_handler(error)

    # start the bot

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()


dispatcher = updater.dispatcher


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()
updater.idle()











