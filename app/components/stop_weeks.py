import asyncio
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message   

import app.components.keyboards as kb 

stop_weeks = Router(name='stop_weeks')

@stop_weeks.message(Command('stop_weeks'))
async def get_help(message:Message):
    await message.answer("this command /stop_weeks")
