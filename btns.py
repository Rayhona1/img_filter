from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def start_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn.add(
        KeyboardButton(text="✨ Rasimga effect berish"),
        KeyboardButton(text="👤 Adminga yozish"),
    )
    # btn.add(
    #     KeyboardButton(text="Ortga"),
    # )
    return btn

async def filters_btn(filters: list):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn.add(
        *[KeyboardButton(text=item) for item in filters]   
    )
    

    btn.add(
        KeyboardButton(text="Ortga"),
    )
    return btn

async def cancel_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(
        KeyboardButton(text="Bekor qilish")
    )
    return btn