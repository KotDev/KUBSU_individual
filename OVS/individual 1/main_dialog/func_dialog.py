import asyncio

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from result_dialog.states import ResultDialog
from main_dialog.states import StartDialog
from result_dialog.func_dialog import background


async def input_message(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    if manager.is_preview():
        await manager.next()
        return
    num = message.text
    if message.text.startswith("-"):
        num = message.text[1:]
    if not num.isdigit():  # Валидация по целому числу
        await message.answer("Нужно вводить целое число")
        await manager.switch_to(StartDialog.input_number_1)
        return
    if "number_1" in manager.dialog_data:
        flag = 2
    else:
        flag = 1
    manager.dialog_data[f"number_{flag}"] = int(message.text)  # Записываем число
    await manager.next()  # Переход к следующему окну


async def go_to_result(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    data = bin(manager.dialog_data["number_1"] + manager.dialog_data["number_2"])
    if data[0] == "-":
        summ = data.replace(data[:3], "1 000 0")
    else:
        summ = data.replace(data[:2], "0 000 0")

    await manager.start(ResultDialog.progress)
    manager.dialog_data["result"] = summ
    asyncio.create_task(background(callback, manager.bg()))
