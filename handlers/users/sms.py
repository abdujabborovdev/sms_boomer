from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, message
from states.sms_states import *
from keyboards.inline.menu import *
from loader import *
from handlers.users.sms_boomer import *

router = Router()
from sqlalchemy import select
import asyncio
from database import *


@router.callback_query(F.data == "sms_boom")
async def sms_boom(call: CallbackQuery, state: FSMContext):
    await state.set_state(Nomer_sora.nomer)
    await call.message.answer("""<b>Sms yuborish kerak bolgan nomerni kiriting!</b>

<i>Masalan: <code>+998*********</code></i>""", parse_mode="HTML")


@router.message(Nomer_sora.nomer)
async def nomer_sora(message: Message, state: FSMContext):
    nomer = message.text
    await state.update_data(nomer=nomer)
    await state.set_state(Nomer_sora.son)
    await message.delete()
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass
    await message.answer("""<b>Neshta sms yuborish kerak!</b>

<i>Masalan: <code>15</code></i>""")


@router.message(Nomer_sora.son)
async def nomer_sora(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.delete()
        await message.answer("""<b>Xato! son 0 - yokida kichik bolishi mumkun emas</b>""")
        return
    son = message.text
    await state.update_data(son=son)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        pass
    data = await state.get_data()
    nomer = data['nomer']
    await message.answer(f"""<b>Nomer: {nomer}
Son: {son}</b>

<b>Ushbu malumotlar tog'riligiga ishonch hosil qiling<tg-emoji emoji-id="5406631276042002796">📨</tg-emoji></b>""",
                         reply_markup=tas, parse_mode="HTML")
    await state.set_state(Nomer_sora.holat)


@router.callback_query(F.data == "tasdiq", Nomer_sora.holat)
async def tasdiq(call: CallbackQuery, state: FSMContext):
    await state.update_data(holat="tasdiq")
    data = await state.get_data()
    nomer = data['nomer']
    son = int(data['son'])
    formatted = f"{nomer[:4]} ({nomer[4:6]}) {nomer[6:9]}-{nomer[9:11]}-{nomer[11:13]}"
    await state.clear()
    limit_sec = 3600
    start_time = time.time()
    async with async_session() as session:
        result = await session.execute(select(Users).where(Users.telegram_id == call.from_user.id))
        user = result.scalar_one_or_none()
        if son > user.limit:
            await call.message.edit_text(f"Balansingiz yetarli emas! Yetmayapti: {son - user.limit}")
            return
        user.limit -= son
        await session.commit()
        await call.message.edit_text(
            f"""{formatted} {son} Sms yuborish boshlandi<tg-emoji emoji-id="5386367538735104399">⌛</tg-emoji>""",
            parse_mode="HTML")
    qoldi = son
    yuborildi = 0
    try:
        while qoldi > 0:
            if (time.time() - start_time) > limit_sec:
                await call.message.answer(f"""⚠️ Vaqt limit tugadi, jarayon avtomatik to'xtatildi! 
Qolgan {qoldi} limitingiz qaytarildi!""")
                async with async_session() as session:
                    user = await session.get(Users, call.from_user.id)
                    user.limit += qoldi
                    await session.commit()
                break
            holat, info = await asyncio.to_thread(send_sms, phone=nomer, formatted_phone=formatted,neshta=yuborildi)
            if holat:
                qoldi = qoldi - 1
                yuborildi = yuborildi + 1
                await call.message.edit_text(f"{info}")
            else:
                await call.message.edit_text(f"{info}")
            await asyncio.sleep(5)
        await call.message.answer(f"""Smslar muvafiyaqiyatlik yuborilindi {yuborildi}-ta""")

    except Exception as e:
        await call.message.answer(F"Xatolik - {e}")


@router.callback_query(Nomer_sora.holat, F.data == "bekor")
async def bekor_qilish(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Amal bekor qilindi.")
    await state.clear()