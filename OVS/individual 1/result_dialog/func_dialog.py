import asyncio

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, BaseDialogManager
from aiogram_dialog.widgets.kbd import Button
from result_dialog.states import ResultDialog


async def get_bg_data(dialog_manager: DialogManager, **kwargs) -> dict:
    """
    :param dialog_manager:
    :param kwargs:
    :return:

    getter для процесса загрузки
    """
    return {"progress": dialog_manager.dialog_data.get("progress", 0)}


async def background(callback: CallbackQuery, manager: BaseDialogManager) -> None:
    """
    :param callback:
    :param manager:
    :return:

    Функция визуализации процесса
    """
    count = 10
    for i in range(1, count + 1):
        await asyncio.sleep(0.5)
        await manager.update(
            {
                "progress": i * 100 / count,
            }
        )
    await asyncio.sleep(0.5)
    await manager.switch_to(ResultDialog.result)


async def get_sum_view(callback: CallbackQuery, button: Button, manager: DialogManager):
    option = button.widget_id
    data = manager.dialog_data["result"]
    table_value = {
        1: ("❌", "✅"),
        2: ("0️⃣", "1️⃣"),
        3: ("0", "1")
    }
    res = ""
    option_value = table_value[int(option)]
    for i in data:
        match i:
            case "0":
                res += option_value[0]
            case "1":
                res += option_value[1]
    manager.dialog_data["option_res"] = res
