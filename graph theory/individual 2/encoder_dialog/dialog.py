from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, SwitchTo, Button
from aiogram_dialog.widgets.text import Const, Format
from encoder_dialog.states import EncoderStates
from aiogram.types import ContentType
from aiogram_dialog.widgets.media import StaticMedia
from encoder_dialog.func_dialog import input_message, get_tree_image, delete_image, go_to_main


encode_dialog = Dialog(
    Window(
        Const("Введите текст который хотите зашифровать"),
        MessageInput(input_message, content_types=[ContentType.TEXT]),
        Button(Const("В главное меню 🏠"), id="main_back", on_click=go_to_main),
        state=EncoderStates.input_state,
    ),
    Window(
        Const("Текст был закодирован, можете посмотреть все данные о кодировке"),
        SwitchTo(Const("Исходное сообщение 📬"), id="input_text", state=EncoderStates.text_state),
        SwitchTo(Const("Закодированное сообщение 📪"), id="code_text", state=EncoderStates.code_state),
        SwitchTo(Const("Дерево Хаффмана 🌳"), id="media", on_click=get_tree_image, state=EncoderStates.tree_state),
        SwitchTo(Const("Таблица кодировки 📁"), id="table_encoder", state=EncoderStates.table_state),
        Back(text=Const("Назад ➡️"), on_click=delete_image),
        state=EncoderStates.result_state,
    ),
    Window(
        Format("Исходный текст: {dialog_data[text]}"),
        SwitchTo(text=Const("Назад ➡️"), state=EncoderStates.result_state, id="back"),
        state=EncoderStates.text_state
    ),
    Window(
        Format("Закодированный текст: {dialog_data[code]}"),
        SwitchTo(text=Const("Назад ➡️"), state=EncoderStates.result_state, id="back"),
        state=EncoderStates.code_state
    ),
    Window(
        StaticMedia(
                path=Format('/home/danil/PycharmProjects/KUBSU_ndividual/graph theory/individual 2/tree_encoder_image_{dialog_data[image_id]}.png'),
                type=ContentType.PHOTO,
            ),
        SwitchTo(text=Const("Назад ➡️"), state=EncoderStates.result_state, id="back"),
        state=EncoderStates.tree_state
    ),
    Window(
        Format("Таблица коддировки:\n {dialog_data[encoder_table]}"),
        SwitchTo(text=Const("Назад ➡️"), state=EncoderStates.result_state, id="back"),
        state=EncoderStates.table_state
    ),
)