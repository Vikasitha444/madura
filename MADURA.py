import logging
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)







keyboard_layout = [InlineKeyboardButton("Option 1", callback_data='1')]


def dictionary(update,context):
    chat_id = update.message.chat.id
    recvied_text = update.message.text

    word = quote(recvied_text)
    url_to_scrape = Request(f'https://www.maduraonline.com/?find={word}', headers={'User-Agent': 'Mozilla/5.0'})

    requested_page = urlopen(url_to_scrape)
    page_html = requested_page.read()
    requested_page.close()

    html_soup = BeautifulSoup(page_html,"html.parser")
    definitions = html_soup.find_all('td', class_ = 'td') #SCRAPPED DATA IN A LIST
    word_classes = html_soup.find_all('td', class_ = 'ty')
    what_did_you_mean = html_soup.find_all('p', class_ = 'pt') #SCRAPPED DATA IN A LIST


    result = ''
    if len(what_did_you_mean) == 0:
        for i in range(len(word_classes[1:])):
            #print(word_classes[i].get_text() ,definitions[i].get_text())
            result = result + word_classes[i].get_text() + ' ' + definitions[i].get_text() + '\n'
        context.bot.send_message(chat_id=chat_id, text= f'<b><u>{recvied_text}</u></b>\n{result}', parse_mode= ParseMode.HTML)

    else:
        keyboard_layout = []
        keyboard = []

        select_definition = html_soup.find_all('a')

        for i in select_definition:
            if i.get_text() != 'Privacy Policy' and i.get_text() !='Next':
                print(i.get_text())

                keyboard_keydata = [InlineKeyboardButton(i.get_text(), callback_data=i.get_text())]
                keyboard.append(keyboard_keydata)

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f'''<b>Nothing found for: 🤷‍♂️</b>\n<i>"{recvied_text}"</i>\n\n<b>What did you mean? 👇</b>''', reply_markup=reply_markup ,parse_mode= ParseMode.HTML)








def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    #query.edit_message_text(text=f"Selected option: {query.data}")


    word = quote(query.data)

    url_to_scrape = Request(f'https://www.maduraonline.com/?find={word}', headers={'User-Agent': 'Mozilla/5.0'})

    requested_page = urlopen(url_to_scrape)
    page_html = requested_page.read()
    requested_page.close()

    html_soup = BeautifulSoup(page_html,"html.parser")
    definitions = html_soup.find_all('td', class_ = 'td') #SCRAPPED DATA IN A LIST
    word_classes = html_soup.find_all('td', class_ = 'ty')

    result = ''

    for i in range(len(word_classes[1:])):
        #print(word_classes[i].get_text() ,definitions[i].get_text())
        result = result + word_classes[i].get_text() + ' ' + definitions[i].get_text() + '\n'
    query.edit_message_text(text=f'<b><u>{query.data}</u></b>\n{result}', parse_mode= ParseMode.HTML)





def start(update,context):
   chat_id = update.message.chat.id
   context.bot.send_message(chat_id=chat_id, text='<b>Enter the word.</b><i> (You can send both Sinhala and English words to find a meaning.)</i>',parse_mode= ParseMode.HTML)






def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("")




def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1917118521:AAErG2kqTaMxQfVwxgHwJqcUqMf9WvUIqPs")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, dictionary))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()


##Madura Dictionary Horoku account details.
##
##Email
##vikasitha4444@protonmail.com
##dragonmaster04@
##
##Horoku Account
##vikasitha4444@protonmail.com
##dragonmaster04@