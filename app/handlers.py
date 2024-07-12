import asyncio
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message

router = Router()

# command START !
@router.message(CommandStart())
async def  cmd_start(message:Message):
    await message.answer('hi !')

# work with PHOTO
@router.message(F.photo)
async def get_photo(message:Message):
    #  тут получаю id photo  await message.answer(f"ID photo {message.photo[-1].file_id}")
    await message.answer_photo(photo = message.photo[-1].file_id , caption="I do not with photos")

# command F 
@router.message(F.text == 'как дела?')
async def how_are_you(message:Message):
    await message.answer('ok!')

# command HELP !
@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer("this command /help")
