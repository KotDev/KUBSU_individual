from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from main_dialog.dialog import start_dialog
from result_dialog.dialog import result_dialog
from main_dialog.states import StartDialog
router = Router()
router.include_routers(
    start_dialog, result_dialog
)

@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(StartDialog.input_number_1, mode=StartMode.RESET_STACK)