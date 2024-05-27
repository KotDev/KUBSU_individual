from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from main_dialog.states import MainState
from main_dialog.func_dialog import go_to_encoder, go_to_decoder
start_dialog = Dialog(
    Window(
        Format("Выберите один из предложенных вариантов"),
        Button(Const("Шифровать 🔒"), id="encode", on_click=go_to_encoder),
        Button(Const("Дешифровать 🔐"), id="decode", on_click=go_to_decoder),
        state=MainState.main
    )
)