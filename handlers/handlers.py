from aiogram import F, Router, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated, ReplyKeyboardRemove
from aiogram.types import Message, CallbackQuery
from aiogram.methods import DeleteMessage
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from common.admins import admin_1
from quest.quests import *
from quest.answers import *

router = Router()

# Определяем состояния
class LevelStates(StatesGroup):
    level_1 = State()
    level_2 = State()
    level_3 = State()
    level_4 = State()
    level_5 = State()
    level_6 = State()
    game_completed = State()


# Приветствие
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    await event.answer(f"Привет, *{event.new_chat_member.user.first_name}*!")

# Прощание
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdated):
    await event.answer(f"Пока, *{event.old_chat_member.user.first_name}*")

#Отправка сообщения админу в лс через бота
@router.message(Command('help'))
async def beauty(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if message.from_user.id == admin_1:
        await message.reply('Тебе не нужна моя помощь! Ты админ!')
    elif current_state is None:
        await message.answer('На этом уровне не предусмотрены подсказки...')
    else:
        await message.answer('Ща-ща')
        await bot.send_message(chat_id=admin_1, text='Красавчик, нужна твоя помощь!')

# Команда /start
@router.message(StateFilter(None), CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if message.from_user.id == admin_1:
        await state.set_state(LevelStates.level_1)
        await message.answer('✅ Игра началась!')
        await message.answer(quest_1) # 1 задание
    else:
        await message.reply('❌ Начать игру может только админ...')

@router.message(LevelStates.level_1, F.text)
async def process_answer(message: Message, state: FSMContext):
    if message.text == answer_1:
        await state.set_state(LevelStates.level_2)
        await message.reply('✅ Код принят!')
        await message.answer(quest_2) # 2 задание
    else:
        await message.reply('❌ Код не принят!')


