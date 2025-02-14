import os
import asyncio

#сначала пишем это в терминал: pip install aiogram
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.client.default import DefaultBotProperties

#импорт роутера
from handlers.handlers import router

#pip install python-dotenv и сохраняем TOKEN=... в файл .env чтобы спрятать его
from dotenv import find_dotenv, load_dotenv

from common.bot_cmds_list import bot_commands

load_dotenv(find_dotenv())

#нужно создать файл '.env' как в примере '.env.example'
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT) #стратегия - состояние чата как одного человека
dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=bot_commands)
    #await bot.set_my_commands(commands=bot_commands, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')