from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler

from dictionary_file import DictionaryFile
from phone_record import PhoneRecord

dictionary = DictionaryFile()


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dictionary.records.append(PhoneRecord(update.message.text))
    dictionary.update()
    await update.message.reply_text('Контакт успешно создан')
    keyboard = [
        [
            InlineKeyboardButton('Показать все', callback_data='/show_all'),
            InlineKeyboardButton('Очистить', callback_data="/clean_all"),
            InlineKeyboardButton('Создать контакт', callback_data="/create")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    lines = ""
    for record in dictionary.records:
        lines += f"{record.to_string()}\n"
    await update.message.reply_text(text=lines, reply_markup=markup)


async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update)

    keyboard = [
        [
            InlineKeyboardButton('Показать все', callback_data='/show_all'),
            InlineKeyboardButton('Очистить', callback_data="/clean_all"),
            InlineKeyboardButton('Создать контакт', callback_data="/create")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    await query.answer()

    if query.data.__contains__('show_all'):
        if len(dictionary.records) <= 0:
            await query.edit_message_text(text=f"Справочник пуст", reply_markup=markup)
        else:
            lines = ""
            for record in dictionary.records:
                lines += f"{record.to_string()}\n"
            await query.edit_message_text(text=lines, reply_markup=markup)
    elif query.data.__contains__('clean_all'):
        dictionary.clean()
        await query.edit_message_text(text='Справочник очищен', reply_markup=markup)
    elif query.data.__contains__('create'):
        creating_file = 1
        await query.edit_message_text(text='Укажите контакт в формате: (ИМЯ#ТЕЛЕФОН)', reply_markup=markup)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Добро пожаловать, {update.effective_user.first_name}')

    keyboard = [
        [
            InlineKeyboardButton('Показать все', callback_data='/show_all'),
            InlineKeyboardButton('Очистить', callback_data="/clean_all"),
            InlineKeyboardButton('Создать контакт', callback_data="/create")
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Используйте главное меню для управления телефонной книгой', reply_markup=markup)


def start():
    app = ApplicationBuilder().token("6528186496:AAGq7CgGeXGZrY86XoxLDjZLTOhq6WuYkdc").build()
    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CallbackQueryHandler(query_handler))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.run_polling()


if __name__ == '__main__':
    start()
