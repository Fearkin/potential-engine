import logging
from os import getenv

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ContentType
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, StartMode, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

storage = MemoryStorage()
bot = Bot(token=getenv("BOT_TOKEN"))
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


class MySG(StatesGroup):
    main = State()


main_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MySG.main,
)
dialog = Dialog(main_window)
registry.register(dialog)


@dp.message_handler(commands=["start"])
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


@dp.message_handler(content_types=ContentType.TEXT)
async def echo_name(message: Message):
    await message.answer(message.chat.id)

'''
@dp.message_handler(filters.RegexpCommandsFilter(
        regexp_commands=[r"(\d+) (\w+)( \w+)?"]
))
async def add_record(message: Message):
    message.answer("test record")
'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)