from aiogram.fsm.state import StatesGroup, State


class MainState(StatesGroup):
    """Состояния главного диалога"""
    main = State()