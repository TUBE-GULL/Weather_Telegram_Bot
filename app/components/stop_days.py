import asyncio
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message   

import app.components.keyboards as kb 

stop_days = Router(name='stop_days')


@stop_days.message(Command('stop_days'))
async def get_help(message:Message):
    await message.answer("this command /stop_days")
