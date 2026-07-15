from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select
from database import Users, async_session
import os

router = Router()

# Adminlar ID sini env'dan o'qib olish
ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS", "").split(",") if admin_id]


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Siz admin emassiz!")
        return

    # Bazadan o'qib olish
    try:
        async with async_session() as session:
            # Users modelidan barcha ma'lumotlarni so'raymiz
            result = await session.execute(select(Users))
            users = result.scalars().all()

            if not users:
                await message.answer("Bazada foydalanuvchilar yo'q.")
                return

            # Ma'lumotlarni chiqarish
            user_list = "👥 **Barcha foydalanuvchilar:**\n\n"
            for user in users:
                # database.py dagi haqiqiy maydon nomlarini ishlatamiz
                user_list += f"Telegram ID: {user.telegram_id} | Nomi: {user.full_name} | Limit: {user.limit}\n"

            await message.answer(user_list)

    except Exception as e:
        await message.answer(f"Bazadan o'qishda xatolik: {e}")