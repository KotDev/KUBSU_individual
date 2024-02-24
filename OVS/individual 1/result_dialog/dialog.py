from result_dialog.states import ResultDialog
from result_dialog.func_dialog import get_bg_data, get_sum_view
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Start, Back
from aiogram_dialog.widgets.text import Const, Progress, Multi, Format
from main_dialog.states import StartDialog

"""Окна диалога event result"""

result_dialog = Dialog(
    Window(
        Multi(
            Const("Высчитываю...."),
            Progress("progress", 10),
        ),
        state=ResultDialog.progress,
        getter=get_bg_data,
    ),
    Window(
        Const("Для просмотра результата выберете один из вариантов"),
        Row(
            SwitchTo(
                Const("1 Вариант"),
                id="1",
                state=ResultDialog.get_format_text_option,
                on_click=get_sum_view,
            ),
            SwitchTo(
                Const("2 Вариант"),
                id="2",
                state=ResultDialog.get_format_text_option,
                on_click=get_sum_view,
            ),
            SwitchTo(
                Const("3 Вариант"),
                id="3",
                state=ResultDialog.get_format_text_option,
                on_click=get_sum_view,
            ),
        ),
        Start(Const("Назад к вводу 1 числа"), id="go_to_start", state=StartDialog.input_number_1),
        state=ResultDialog.result,
        ),
    Window(
        Format("{dialog_data[option_res]}"),
        Back(text=Const("Back")),
        state=ResultDialog.get_format_text_option,
    ),
)
