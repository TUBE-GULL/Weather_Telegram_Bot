import aiosqlite 

class DataBase:
    
    def __init__(self, db_name='./db/DataBase.db'):
        self.db_name = db_name


    async def create_table(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                             CREATE TABLE IF NOT EXISTS  data_users(
                                user_id INTEGER PRIMARY KEY,
                                user_name TEXT,
                                language TEXT DEFAULT RU,
                                time_zone INTEGER,
                                city  TEXT,
                                coordinates TEXT,
                                alarm_day INTEGER,
                                alarm_week INTEGER,
                                question TEXT
                             );
                             ''')
            await db.commit()


    async def add_user_database(self, user_id:int, user_name:str, language:str):
        async with  aiosqlite.connect(self.db_name) as db:
            await db.execute('''INSERT OR IGNORE INTO data_users
                            (user_id, user_name, language)
                            VALUES (?,?,?)''',(user_id, user_name, language)) 
            await db.commit()



    async def write_database(self, user_id:int, value:any, column:str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(f'UPDATE data_users SET {column}=? WHERE user_id=?',
                             (value, user_id))
            await db.commit()


    async def read_database(self, user_id: int, column:str):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(f'SELECT {column} FROM data_users WHERE user_id = ?', (user_id,)) as cursor:
                results = await cursor.fetchone()
                if results is not None:
                    return results[0]
                else:
                    return None 


    #fun for Newsletter
    async def get_all_users_with_time(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT user_id, time_zone, alarm_day, alarm_week FROM data_users") as cursor:
                rows = await cursor.fetchall()
                return rows
        
        
        
