import logging
from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import *
from utils import *
from btns import *
from database import *
import os


BOT_TOKEN = "6704159993:AAGQex8YxXc8W2V4xtMlA0M7B6UTFvyFISg"
ADMINS = [1193762770]

logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN, parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot=bot , storage=storage)



async def set_commands(dp: Dispatcher):
    await create_tables()
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Ishga tushirish"),
        ]
    )



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    btn = await start_btn()
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer("Hello" , reply_markup=btn)


@dp.message_handler(commands=['stat'])
async def get_user_stat_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        counts = await get_all_users()
        await message.answer(f"Bot azolar soni: {counts} ta")

@dp.message_handler(text="✨ Rasimga effect berish")
async def effect_to_image_handler(message: types.Message):
    btn = await filters_btn(filters)
    await message.answer("Filterni tanlang", reply_markup=btn)

@dp.message_handler(text="Ortga")
async def back_handler(message: types.Message):
    btn = await start_btn()
    await message.answer("Ortga qaytingiz", reply_markup=btn)

@dp.message_handler(state=UserStates.get_image, content_types=['photo', 'text'])
async def get_image_handler(message:types.message, state:FSMContext):
    content = message.content_type

    if content == "text":
        await effect_to_image_handler(message)
    else:
        filename = f"rasim_{message.from_user.id}.jpg"
        await message.photo[-1].download(destination_file=filename)
    await message.answer("Rasim qabul qilindi!")

    data = await state.get_data()
    await filter_user_image(filename, filter=data['filter'])
    await message.answer_photo(
        photo=types.InputFile(filename),
        caption = f"RAsim tayyor"
    )
    os.remove(filename)
    await start_command(message)
    await state.finish()


    

@dp.message_handler(content_types=['text'])
async def selected_filter_handler(message: types.Message, state: FSMContext):
    text = message.text

    if text in filters:
        await state.update_data(filter=text)
        btn = await cancel_btn()
        await message.answer("Rasimni yuboring:", reply_markup=btn)
        await UserStates.get_image.set()



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_commands)
