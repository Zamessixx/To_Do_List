from aiogram import Dispatcher, Bot, executor, types
from config import API_KEY
import database

bot = Bot(token= API_KEY)
dp = Dispatcher(bot)


database.init_db()

@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.reply('Привет, я бот который может добавлять ваши задачи или напоминание')



@dp.message_handler(commands= 'add')
async def add(message: types.Message):
    task = message.get_args()
    if task:
        user_id = message.from_user.id
        username = message.from_user.username
        database.add_task(user_id, username, task)
        await message.reply(f"Задача{task} добавлена")
    else:
        await message.reply('Пожалуйста, укажите команду через команду /add')


@dp.message_handler(commands='list')
async def list(message: types.Message):
    tasks = database.get_task()
    if tasks:
        tasks_list = "\n".join([f"{task[0]}. {task[3]} (Добавлена пользователем @{task[2]})" for task in tasks])
        await message.reply(f"Ваши задачи: \n{tasks_list}")
    else:
        await message.reply('У вас нету задач')

@dp.message_handler(commands='delete')
async def delete(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        database.delete_task(int(task_id))
        await message.reply(f"Задача удалена{task_id} удалена")
    else:
        await message.reply('Укажите корректный id задач')





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)