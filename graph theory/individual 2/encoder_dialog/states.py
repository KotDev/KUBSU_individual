from aiogram.fsm.state import StatesGroup, State


class EncoderStates(StatesGroup):
    """Состояния диалога шифрования"""
    input_state = State()
    result_state = State()
    code_state = State()
    text_state = State()
    table_state = State()
    tree_state = State()
    table_frequency = State()
