from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config.config import settings


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Бот запущен!")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "Добавить источник",
        "Новости за последний час",
        "Новости за последние сутки",
        "Помощь"
    ]
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Новости за последний час")
async def get_news_hour(message: types.Message):
    user_id = message.from_user.id
    await send_to_queue(user_id)
    await message.answer("Ваш запрос на новости за последний час принят!")


@dp.message_handler(lambda message: message.text == "Новости за последние сутки")
async def get_news_day(message: types.Message):
    user_id = message.from_user.id
    await send_to_queue(user_id)
    await message.answer("Ваш запрос на новости за последние сутки принят!")


@dp.message_handler(lambda message: message.text == "Добавить источник")
async def add_source(message: types.Message):
    await message.answer("Введите URL источника для добавления:")


@dp.message_handler(lambda message: message.text == "Помощь")
async def help_command(message: types.Message):
    await message.answer("Вы можете использовать следующие команды:\n"
                         "/start - начать\n"
                         "Добавить источник - добавить новый источник\n"
                         "Новости за последний час - получить новости за последний час\n"
                         "Новости за последние сутки - получить новости за последние сутки")
