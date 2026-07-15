from aiogram.fsm.state import State, StatesGroup


class Tolov(StatesGroup):
    limit = State()
    check = State()