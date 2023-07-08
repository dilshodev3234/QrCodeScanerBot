from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from bot.dispatcher import dp
from db.model import Qrcodes, Users


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext): 
    deep_user = msg.get_args()
    if deep_user != "":
        qrcodes = Qrcodes('active').select(int(deep_user)).fetchone()
        if qrcodes:
            if qrcodes[0]:
                await msg.answer(text=f"<b>Bu QR-code ishlatilgan!</b>", parse_mode="HTML")
                await state.finish()
            else:
                await msg.answer_photo(photo= "https://telegra.ph/file/d2a51afb3fab6e7c0c95e.png",
                    caption=f"""<b>Assalomu aleykum hurmatli mijoz!
Ishtirokchiga aylanish uchun ISM SHARIFINGIZNI va TELAFON RAQAMINGIZNI kiriting!
</b>""",
                    parse_mode="HTML")
                await state.set_state("name")
                async with state.proxy() as data:
                    data["qrcode_id"] = deep_user
                Qrcodes().update(qrcode_id=deep_user, active=True)
                await msg.answer(text=f"<b>Ro'yhatdan o'tishni boshlimiz 😊</b>", parse_mode="HTML")
                await msg.answer(text=f"<b>Ismingizni kiriting ✍️:</b>", parse_mode="HTML")



@dp.message_handler(state='name')
async def name_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await state.set_state("phone")
    await msg.answer(text=f"<b>Telefon raqamingizni kiriting ☎️:</b>", parse_mode="HTML")


@dp.message_handler(state='phone')
async def phone_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = msg.text
    text = """Siz BONVI Aksiyasi ishtirokchisi bo’dingiz! Aksiya tugagunga qadar QR-kodingizni tashlab yubormang!

Aksiya 25 sentabr kuni yakunlanadi!
30 sentabr kuni jonli efirda o’ynaladi, aloqada bo’ling! OMAD!"""
    await msg.answer(text=f"<b>{text}</b>", parse_mode="HTML")
    await state.finish()
    Users().insert_into(user_id=str(msg.from_user.id), name=data['name'], phone=data['phone'], qrcode_id=data['qrcode_id'])
