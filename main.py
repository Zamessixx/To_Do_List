from aiogram import Dispatcher, Bot, executor, types
from config import API_KEY
import database

bot = Bot(token= API_KEY)
dp = Dispatcher(bot)


database.init_db()




async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='команда для активации'),
        types.BotCommand(command='/add', description='команда для доблавление задачи'),
        types.BotCommand(command='/list', description='команда для того чтобы показать список задач'),
        types.BotCommand(command='/delete', description='команда для удаление задача')
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.reply('Привет, я бот который может добавлять ваши задачи или напоминание')



@dp.message_handler(commands='add')
async def add(message: types.Message):
    task = message.get_args()
    if task:
        user_id = message.from_user.id
        user_name = message.from_user.username
        existing_tasks = database.get_task()
        if any(task in t for t in existing_tasks):
            await message.reply(f"Задача {task} уже существует")
        else:
            database.add_task(user_id, user_name, task)
            await message.reply(f"Ваша задача {task} добавлена")


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


async def on_startup(dispatcher):
    await set_commands(dispatcher.bot)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True, on_startup=on_startup)