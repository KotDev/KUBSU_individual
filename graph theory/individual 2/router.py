from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from main_dialog.dialog import start_dialog
from encoder_dialog.dialog import encode_dialog
from decoder_dialog.dialog import decode_dialog
from main_dialog.states import MainState
router = Router()
router.include_routers(
    start_dialog, encode_dialog, decode_dialog
)


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainState.main, mode=StartMode.RESET_STACK)