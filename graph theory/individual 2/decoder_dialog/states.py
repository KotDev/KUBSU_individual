from aiogram.fsm.state import StatesGroup, State


class StateDecoder(StatesGroup):
    """Состояния декодера"""

    input_table = State()
    input_code = State()
    result = State()
    decoder_result = State()
    encoder_message = State()
    tree_decoder = State()
    table_encoder = State()
    table_frequency_decoder = State()