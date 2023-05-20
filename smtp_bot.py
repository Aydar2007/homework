from aiogram import Bot, Dispatcher,executor, types
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import sqlite3, logging, smtplib, os
from smtp_py import send_mail

load_dotenv(".env")

bot = Bot(os.environ.get("token"))
storage=MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

db3 = sqlite3.connect('database.db')
cursor = db3.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS title(
    id INT,
    mail VARCHAR(150),
    subject VARCHAR(1000),
    message1 VARCHAR(1000)
);
""")
cursor.connection.commit()

class EmailState(StatesGroup):
    mail = State()
    subject = State()
    message1 =State()

inline_keyboards=[
    InlineKeyboardButton('Отправить сообщение',callback_data="send_mail")
]

inline = InlineKeyboardMarkup().add(*inline_keyboards)


@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer("Hello World",reply_markup=inline)

@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == "send_mail":
        await send_bot_mail (call.message)
    
@dp.message_handler(commands="send")
async def send_bot_mail(message:types.Message):
    await message.answer("Почта:")
    await EmailState.mail.set()

@dp.message_handler(state=EmailState.mail)
async def get_subject(message:types.Message,state:FSMContext):
    await state.update_data(mail=message.text)
    await message.answer("Введите заголовок:")
    await EmailState.subject.set()

@dp.message_handler(state=EmailState.subject)
async def get_subject(message:types.Message,state:FSMContext):
    await state.update_data(mail=message.text)
    await message.answer("Введите сообщение:")
    await EmailState.message1.set()



@dp.message_handler(state=EmailState.message1)
async def send_message(message:types.Message, state:FSMContext):
    await state.update_data(message=message.text)
    mail_data = await storage.get_data(user=message.from_user.id)
    # cursor = db3.cursor()
    # cursor.execute(f"""INSERT INTO title VALUES(
    #     {message.from_user.id},
    #     '{mail_data["mail"]}',
    #     '{mail_data["subject"]}',
    #     '{mail_data["message1"]}'
    # );""")
    # cursor.connection.commit()
    # sql = '''SELECT mail FROM title  WHERE id={message.from.user_id};'''
    # cursor.execute(sql)
    # rows = cursor.fetchall()
    # for row in rows:
    #     mail=row
    #     sql = '''SELECT subject FROM title  WHERE id={message.from.user_id};'''
    # cursor.execute(sql)
    # rows = cursor.fetchall()
    # for row in rows:
    #     subject=row
    #     sql = '''SELECT message1 FROM title  WHERE id={message.from.user_id};'''
    # cursor.execute(sql)
    # rows = cursor.fetchall()
    # for row in rows:
    #     message1=row
    print(send_mail({mail_data["message1"]},{mail_data['subject']},{mail_data["mail"]}))




executor.start_polling(dp,skip_updates=True)