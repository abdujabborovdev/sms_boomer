from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="SMS yuborish",callback_data="sms_boom",icon_custom_emoji_id='5276032951342088188'),InlineKeyboardButton(text="Limit olish",callback_data="tolov",icon_custom_emoji_id='5375296873982604963')]

])


tas = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Tasdiqlash",callback_data="tasdiq",icon_custom_emoji_id='5427009714745517609')],
    [InlineKeyboardButton(text="Bekor qilish",callback_data="bekor",icon_custom_emoji_id='5341806819247401359')],
])


karta = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="UzCard",callback_data="uzcard",icon_custom_emoji_id='5404877477686300726')],
    [InlineKeyboardButton(text="Humo",callback_data="humo",icon_custom_emoji_id='5404672397292883011')],
])

def admin_confirm_keyboard(user_id, limit):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_{user_id}_{limit}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_{user_id}")
        ]
    ])