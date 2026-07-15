from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup
from sqlalchemy import select
from database import *
from keyboards.inline.menu import *

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message):
    async with async_session() as session:
        # Foydalanuvchini bazadan qidiramiz
        result = await session.execute(select(Users).where(Users.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()

        if user is None:
            new_user = Users(telegram_id=message.from_user.id, full_name=message.from_user.full_name,
                             limit=2)  # limitni 0 deb belgilashni unutmang
            session.add(new_user)
            await session.commit()

            # Yangi foydalanuvchi uchun limitni 0 deb qabul qilamiz
            current_limit = 0

            await message.answer(
                f"""Salom, {message.from_user.full_name}!\n\n<b>Sms Boom - <tg-emoji emoji-id="5303112793157810087">💣</tg-emoji> Botiga xush kelibsiz <tg-emoji emoji-id="5472055112702629499">👋</tg-emoji></b>\n\nID: {message.from_user.id}\nLimit: {current_limit}""",
                parse_mode="HTML", reply_markup=menu)

        else:
            # Bazada bo'lsa, bazadan olingan limitni chiqaramiz
            await message.answer(
                f"""Salom, {message.from_user.full_name}!\n\n<b>Sms Boom - <tg-emoji emoji-id="5303112793157810087">💣</tg-emoji> Botiga xush kelibsiz <tg-emoji emoji-id="5472055112702629499">👋</tg-emoji></b>\n\n<b>ID</b> - <code>{message.from_user.id}</code>\n<b>Limit</b>: {user.limit}""",
                parse_mode="HTML", reply_markup=menu)