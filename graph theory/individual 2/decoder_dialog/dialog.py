from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Back
from aiogram_dialog.widgets.text import Const, Format
from aiogram.types import ContentType
from aiogram_dialog.widgets.media import StaticMedia
from decoder_dialog.states import StateDecoder
from decoder_dialog.func_dialog import (input_message_code, input_message_table,
                                        delete_image, get_tree_decoder_image, go_to_main)

decode_dialog = Dialog(
    Window(
        Const("Введите таблицу частот"),
        MessageInput(input_message_table, content_types=[ContentType.TEXT]),
        Button(Const("В главное меню 🏠"), id="main_back", on_click=go_to_main),
        state=StateDecoder.input_table,
    ),
    Window(
        Const("Введите код закодированного слова"),
        MessageInput(input_message_code, content_types=[ContentType.TEXT]),
        Back(Const("Назад ➡️"), id="main_back"),
        state=StateDecoder.input_code
    ),
    Window(
        Const("Выбирете один из предложенных вариантов"),
        SwitchTo(Const("Исходное закодированное сообщение 📪"), id="encoder_text", state=StateDecoder.encoder_message),
        SwitchTo(Const("Декодируемое сообщение 📬"), id="decoder_message", state=StateDecoder.decoder_result),
        SwitchTo(Const("Таблица частот 📊"), id="table_frequency", state=StateDecoder.table_frequency_decoder),
        SwitchTo(Const("Дерево Хаффмана 🌳"), id="tree_decoder", state=StateDecoder.tree_decoder, on_click=get_tree_decoder_image),
        SwitchTo(Const("Таблица кодировки 📁"), id="table_encoder_text", state=StateDecoder.table_encoder),
        Back(Const("Назад ➡️"), on_click=delete_image),
        state=StateDecoder.result
    ),
    Window(
        Format("Закодированное сообщение:\n{dialog_data[code_decoder]}"),
        SwitchTo(Const("Назад ➡️"), id="back_result", state=StateDecoder.result),
        state=StateDecoder.encoder_message
    ),
    Window(
        Format("Раскодированное сообщение:\n{dialog_data[text_decoder]}"),
        SwitchTo(Const("Назад ➡️"), id="back_result", state=StateDecoder.result),
        state=StateDecoder.decoder_result
    ),
    Window(
        Format("Таблица частот:\n{dialog_data[table_frequency]}"),
        SwitchTo(Const("Назад ➡️"), id="back_result", state=StateDecoder.result),
        state=StateDecoder.table_frequency_decoder
    ),
    Window(
        Format("Таблица кодировки:\n{dialog_data[encoder_table_sim]}"),
        SwitchTo(Const("Назад ➡️"), id="back_result", state=StateDecoder.result),
        state=StateDecoder.table_encoder
    ),
    Window(
        StaticMedia(
            path=Format(
                '/home/danil/PycharmProjects/KUBSU_ndividual/graph theory/individual 2/tree_decoder_image_{dialog_data[image_decoder_id]}.png'),
            type=ContentType.PHOTO,
        ),
        SwitchTo(text=Const("Назад ➡️"), state=StateDecoder.result, id="back_result"),
        state=StateDecoder.tree_decoder
    ),
)

