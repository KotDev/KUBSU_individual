from aiogram.fsm.state import StatesGroup, State


class StartDialog(StatesGroup):
    """Состояние для диалога start"""

    main = State()
    input_number_1 = State()
    input_number_2 = State()
    examination_num = State()