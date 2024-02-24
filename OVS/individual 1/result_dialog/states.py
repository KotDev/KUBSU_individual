from aiogram.fsm.state import StatesGroup, State


class ResultDialog(StatesGroup):
    """Состояния дя диалога Result"""

    progress = State()
    result = State()
    get_format_text_option = State()