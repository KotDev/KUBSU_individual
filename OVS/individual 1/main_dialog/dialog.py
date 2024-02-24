from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ContentType
from main_dialog.states import StartDialog
from main_dialog.func_dialog import input_message, go_to_result
start_dialog = Dialog(
    Window(
        Const("Введите первое число"),
        MessageInput(input_message, content_types=[ContentType.TEXT]),
        state=StartDialog.input_number_1,
    ),
    Window(
        Format("Введите 2 число {dialog_data[number_1]} + ?"),
        MessageInput(input_message, content_types=[ContentType.TEXT]),
        state=StartDialog.input_number_2
    ),
    Window(
        Format("Вы ввели {dialog_data[number_1]} + {dialog_data[number_2]} = ? "),
        Button(Const("Считать в 2 с/c"), id="start", on_click=go_to_result),
        state=StartDialog.examination_num
    )
)