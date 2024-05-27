import asyncio

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from encoder_dialog.states import EncoderStates
from decoder_dialog.states import StateDecoder


async def go_to_decoder(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    await manager.start(StateDecoder.input_table)


async def go_to_encoder(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    await manager.start(EncoderStates.input_state)
