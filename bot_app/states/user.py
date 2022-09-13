from aiogram.dispatcher.filters.state import StatesGroup, State


class NewApplication(StatesGroup):
    base_menu = State()
    language_data = State()
