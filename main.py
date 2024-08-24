import asyncio
from aiogram import Bot, Dispatcher
from log import my_logo 
from app.components.read_tokens import TOKEN
from app.components.working_db import DataBase
from app.root import router


bot = Bot(token = TOKEN[0])

async def main():
    
    db = DataBase()
    await db.create_table()    

    my_logo.logo()
    
    
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__  == '__main__':
    asyncio.run(main())
    