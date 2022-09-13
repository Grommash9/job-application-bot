import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from bot_app import db, markups, config
from bot_app.misc import bot, dp
from bot_app.models.params import Params
from bot_app.states.user import NewApplication


def get_button_text(reply_markup, callback):
    for buttons_set in reply_markup['inline_keyboard']:
        for buttons in buttons_set:
            if buttons.callback_data == callback:
                return buttons.text


@dp.callback_query_handler(text='start-application')
async def start_application(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(NewApplication.base_menu)

    await call.message.edit_text('Хочешь зарабатывать от 2000$ в месяц?',
                                 reply_markup=markups.user.main.money_markup())


@dp.callback_query_handler(text_startswith='money-', state=NewApplication.base_menu)
async def money_answer_getter(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_data({'application-result':
                          f"{call.message.text}\n"
                          f"<b>{get_button_text(call.message.reply_markup, call.data)}</b>\n\n"})

    await call.message.edit_text('Хочешь переехать в Киев? (Переезд и проживание оплачивается)',
                                 reply_markup=markups.user.main.relocate_markup())


@dp.callback_query_handler(text_startswith='relocate-', state=NewApplication.base_menu)
async def relocate_answer_getter(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    await state.update_data({'application-result': f"{data['application-result']}" +
                              f"{call.message.text}\n"
                              f"<b>{get_button_text(call.message.reply_markup, call.data)}</b>\n"})

    await call.message.edit_text('Сколько полных лет?',
                                 reply_markup=markups.user.main.age_markup())


@dp.callback_query_handler(text_startswith='age-', state=NewApplication.base_menu)
async def age_answer_getter(call: CallbackQuery, state: FSMContext):
    await call.answer()
    jobs_list = await db.job.get_all()
    data = await state.get_data()
    await state.update_data({
        'application-result':
            f"{data['application-result']}\n{call.message.text}\n"
            f"<b>{get_button_text(call.message.reply_markup, call.data)}</b>\n\n",
        'jobs-data': json.dumps(jobs_list)})
    jobs_class_list = Params(jobs_list)
    await call.message.edit_text('Какой есть опыт работы?',
                                 reply_markup=markups.user.main.job_experience(jobs_class_list.param_list))


@dp.callback_query_handler(text_startswith='job-switch', state=NewApplication.base_menu)
async def job_switch_menu(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    jobs_list = json.loads(data['jobs-data'])
    jobs_class_list = Params(jobs_list)
    new_class_list, new_list = jobs_class_list.switch_job(call.data.split('_')[-1])

    await state.update_data({'jobs-data': json.dumps(new_list)})
    await call.message.edit_reply_markup(markups.user.main.job_experience(new_class_list))


@dp.callback_query_handler(text='job-finish', state=NewApplication.base_menu)
async def finish_job_select(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    jobs_list = json.loads(data['jobs-data'])
    jobs_class_list = Params(jobs_list)

    result = jobs_class_list.get_all_enabled_str()

    data = await state.get_data()
    await state.update_data({
        'application-result':
            f"{data['application-result']}{call.message.text}\n<b>{result}</b>\n\n",
        'jobs-data': json.dumps(jobs_list)})

    await call.message.edit_text('Холост или в отношениях?',
                                 reply_markup=markups.user.main.relationship_markup())


@dp.callback_query_handler(text_startswith='relationship-', state=NewApplication.base_menu)
async def get_relationship_answer(call: CallbackQuery, state: FSMContext):
    await call.answer()

    habits_list = await db.habits.get_all()
    data = await state.get_data()
    await state.update_data({
        'application-result':
            f"{data['application-result']}{call.message.text}\n"
            f"<b>{get_button_text(call.message.reply_markup, call.data)}</b>\n\n",
        'habits-data': json.dumps(habits_list)})
    habits_class_list = Params(habits_list)

    await call.message.edit_text('Вредные привычки?',
                                 reply_markup=markups.user.main.bad_habits(habits_class_list.param_list))


@dp.callback_query_handler(text_startswith='habit-switch', state=NewApplication.base_menu)
async def habit_switch_menu(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    habits_list = json.loads(data['habits-data'])
    habits_class_list = Params(habits_list)
    new_class_list, new_list = habits_class_list.switch_job(call.data.split('_')[-1])

    await state.update_data({'habits-data': json.dumps(new_list)})
    await call.message.edit_reply_markup(markups.user.main.bad_habits(new_class_list))


@dp.callback_query_handler(text='finish-habit', state=NewApplication.base_menu)
async def finish_habit_select(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    habits_list = json.loads(data['habits-data'])
    habits_list_class_list = Params(habits_list)

    result = habits_list_class_list.get_all_enabled_str()

    data = await state.get_data()
    await state.update_data({
        'application-result':
            f"{data['application-result']}{call.message.text}\n<b>{result}</b>\n\n"})

    await call.message.delete()
    await state.set_state(NewApplication.language_data)
    await bot.send_message(call.from_user.id,
                           'Расскажите про знание языков:',
                           reply_markup=markups.base.cancel_menu())


@dp.message_handler(state=NewApplication.language_data)
async def get_language_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({
        'application-result':
            f"{data['application-result']}Знание языков:\n<b>{message.text}</b>\n\n"})

    data = await state.get_data()

    await state.finish()

    await bot.send_message(message.from_user.id,
                           'Опрос окончен, спасибо!',
                           reply_markup=ReplyKeyboardRemove())

    if message.from_user.username is None:
        user_data = await db.user.get_user(message.from_user.id)
        contact = f"{message.from_user.full_name} {user_data['phone_number']}"
    else:
        contact = f"{message.from_user.full_name} @{message.from_user.username}"
    await bot.send_message(config.TARGET_CHANNEL,
                           f"<b>Новая заявка!</b> от {contact}\n\n"
                           f"{data['application-result']}")