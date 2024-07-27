import asyncio
from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message   

import app.components.keyboards as kb 

stop = Router(name='stop')


@stop.message(Command('stop'))
async def get_help(message:Message):
    await message.answer("this command /stop")