import datetime
import json

import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot_app import db, markups
from bot_app.misc import bot, dp
from bot_app.models.params import Params
from bot_app.states.user import NewApplication


@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    user_data = await db.user.create_user(message.from_user, message.get_args())
    await state.finish()

    if message.from_user.username is None:
        await bot.send_message(message.from_user.id,
                               'У вас нет имени пользователя и мы не сможем связаться с вами если рассмотрим заявку,'
                               ' пожалуйста установите его,'
                               ' а потом нажмите /start снова или отправьте нам ваш номер телефона',
                               reply_markup=markups.user.main.send_phone_number())
        return

    await bot.send_message(message.from_user.id,
                           'Пройди тест и оставь заявку на работу!\n'
                           'Текст - Работа! (не курсы и не обучение)',
                           reply_markup=markups.user.main.start_application())


@dp.message_handler(content_types=aiogram.types.ContentTypes.CONTACT)
async def get_phone_number(message: Message):
    if message.contact.user_id != message.from_user.id:
        await bot.send_message('Можно отправлять только свой номер!')
        return
    await db.user.set_phone(message.contact.phone_number, message.from_user.id)
    await bot.send_message(message.from_user.id,'Номер телефона принят!',
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id,
                           'Пройди тест и оставь заявку на работу!\n'
                           'Текст - Работа! (не курсы и не обучение)',
                           reply_markup=markups.user.main.start_application())
