import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo
from aiogram.exceptions import TelegramAPIError, AiogramError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token="7375792763:AAHcKU3WQB3gWn7c3zI_iyjX7rx32a5tP6g")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    try:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Выбрать подарок из списка'),
                    KeyboardButton(text='Посмотреть плохие варианты')
                ]
            ],
            resize_keyboard=True
        )
        await message.answer(
            f'Привет, {message.from_user.first_name}! Я попробую помочь с подарком. Что хочешь узнать?',
            reply_markup=markup
        )
    except TelegramAPIError as e:
        logger.error(f"Ошибка в start_handler: {e}")

@dp.message()
async def choice_handler(message: Message):
    try:
        if message.text == 'Выбрать подарок из списка':
            inline_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Варианты до 50 рублей",
                                          web_app=WebAppInfo(url="https://ieeeep.github.io/Wishlist/wishlist.html"))],
                    [InlineKeyboardButton(text="Варианты от 50 рублей",
                                          web_app=WebAppInfo(url="https://ieeeep.github.io/Wishlist/expensiveWish.html"))],
                    [InlineKeyboardButton(text="Книги",
                                          web_app=WebAppInfo(url="https://ieeeep.github.io/Wishlist/books.html"))],
                    [InlineKeyboardButton(text="Варианты для Саши",
                                          web_app=WebAppInfo(url="https://ieeeep.github.io/Wishlist/sasha.html"))]
                ]
            )
            await message.answer(
                "Вот список подарков! Они разбиты по цене на две категории. Кнопка 'Книги' покажет всё, что у меня есть на полке. Если вы решите подарить мне какое-то чтиво, то ознакомьтесь с уже имеющимися.",
                reply_markup=inline_markup
            )
        elif message.text == 'Посмотреть плохие варианты':
            await message.answer("Вот пример того, что бы я не хотела получить.")
            await message.answer(
            inline_keyboard=[
                [InlineKeyboardButton(text="Посмотреть антивишлист",
                                      web_app=WebAppInfo(url="https://ieeeep.github.io/Wishlist/tabu.html"))]
            ])
        else:
            await message.answer("Кис, ты чет не то нажала, попробуй ещё раз.")
    except TelegramAPIError as e:
        logger.error(f"Ошибка в choice_handler: {e}")


async def main():
    try:
        await dp.start_polling(bot)
    except AiogramError as e:
        logger.error(f"Ошибка сети: {e}")
        await asyncio.sleep(5)
        await main()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")