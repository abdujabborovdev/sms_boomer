from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from database import *
from keyboards.inline.menu import *
from states import Tolov
from data.config import *
from loader import *

router = Router()


@router.callback_query(F.data=="tolov")
async def tolov(call: CallbackQuery):
    await call.message.edit_text(f"""<b><tg-emoji emoji-id="5406745015365943482">⬇️</tg-emoji> Pastda berilgan to'lov tizimlardan birini tanlang va to'lov summasini kiriting. Sizga berilgan karta orqali to'lovni amalga oshiring !
    
<blockquote><tg-emoji emoji-id="5215677343594457295">⚠️</tg-emoji> Diqqat! Barcha to'lov tizimlari 100% xavfsiz va qonuniy. Bot hisobidagi pulni qaytarish imkoni yo'q iltimos hisobingizni kerakli miqdorda to'ldiring. <tg-emoji emoji-id="5298502004031646403">❗️</tg-emoji>️</blockquote></b>""",parse_mode="HTML",reply_markup=karta)


@router.callback_query(F.data=="uzcard")
async def uzcard(call: CallbackQuery,state: FSMContext):
    await state.set_state(Tolov.limit)
    await call.message.edit_text(f"""<b><tg-emoji emoji-id="5296565124104993719">💵</tg-emoji> Hisobingzini qancha limitga to'ldirmoqchisiz ?
    
1 limit = 350 uzs

<tg-emoji emoji-id="5406745015365943482">⬇️</tg-emoji> Minimal limit: 5</b>""",parse_mode="HTML")


@router.callback_query(F.data == "humo")
async def uzcard(call: CallbackQuery, state: FSMContext):
    await state.set_state(Tolov.limit)
    await call.message.edit_text(f"""<b><tg-emoji emoji-id="5296565124104993719">💵</tg-emoji> Hisobingzini qancha limitga to'ldirmoqchisiz ?

1 limit = 350 uzs

<tg-emoji emoji-id="5406745015365943482">⬇️</tg-emoji> Minimal limit: 5</b>""", parse_mode="HTML")


@router.message(Tolov.limit)
async def limit(message: Message,state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("Iltimos, faqat musbat raqam kiriting!")
        return

    son = int(message.text)
    summa = 350*son
    await state.update_data(limit=son)
    await state.set_state(Tolov.check)
    await message.answer(f"""<b><tg-emoji emoji-id="5470177992950946662">👇</tg-emoji> To'lov kartalar 
    
<tg-emoji emoji-id="5404877477686300726">💳</tg-emoji>: <code>5614 6835 1424 8970</code>
<tg-emoji emoji-id="5404672397292883011">💳</tg-emoji>: <code>9860 1666 0342 3145</code>

<tg-emoji emoji-id="5296565124104993719">💵</tg-emoji> Miqdori: <code>{summa}</code> so‘m
<tg-emoji emoji-id="5208575215738573162">🧾</tg-emoji> To'lov qilib boʻlganingizdan soʻng chekni shu yerga yuboring</b>""")

@router.message(Tolov.check,F.photo)
async def check(message: Message,state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    limit = int(data.get("limit"))
    summa = 350 * limit
    await state.set_state(Tolov.limit)
    await bot.send_photo(
        chat_id=ADMINS[0],
        photo=photo_id,
        caption=f"Yangi to'lov!\nUser: @{message.from_user.username}\nID: {message.from_user.id}\nLimit: {limit}\nSumma: {summa}",
        reply_markup=admin_confirm_keyboard(message.from_user.id, limit)  # Admin uchun tasdiqlash tugmalari bor menu
    )

    await message.answer("To'lov cheki qabul qilindi. Admin tasdiqlashini kuting.")
    await state.clear()


@router.callback_query(F.data.startswith("confirm_"))
async def approve_payment(callback: CallbackQuery):
    # Data format: "confirm_user_id_limit"
    _, user_id, limit = callback.data.split("_")

    async with async_session() as session:
        # 1. Bazadagi foydalanuvchini topamiz
        result = await session.execute(select(Users).where(Users.telegram_id == int(user_id)))
        user = result.scalar_one_or_none()

        if user:
            # 2. Limitni oshiramiz
            user.limit += int(limit)
            await session.commit()

            # 3. Admin va Userga xabar
            await callback.message.edit_caption(caption=f"✅ Tasdiqlandi! User {user_id} ga {limit} limit qo'shildi.")
            await bot.send_message(chat_id=user_id, text=f"🎉 To'lovingiz tasdiqlandi! Sizga {limit} limit qo'shildi.")


@router.callback_query(F.data.startswith("cancel_"))
async def cancel_payment(callback: CallbackQuery):
    _, user_id = callback.data.split("_")
    await callback.message.edit_caption(caption="❌ To'lov rad etildi.")
    await bot.send_message(chat_id=user_id, text="⚠️ To'lovingiz admin tomonidan rad etildi.")