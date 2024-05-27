import asyncio

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from Haffman import HaffmanTree, Encoder
import os

from main_dialog.states import MainState


async def input_message(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    if manager.is_preview():
        await manager.next()
        return
    tree = HaffmanTree(text=message.text)
    analysis_list = tree.frequency_analysis()
    root_tree = tree.build_tree(analysis_list)
    encoder = Encoder(text=message.text, table=dict())
    encoder.table_haffman(root_tree, "")
    code = encoder.encoder_text()

    manager.dialog_data["encoder_table"] = encoder.view_table()
    manager.dialog_data["root"] = root_tree
    manager.dialog_data["tree"] = tree
    manager.dialog_data["code"] = code
    manager.dialog_data["text"] = message.text
    await manager.next()  # Переход к следующему окну


async def get_tree_image(callback: CallbackQuery, button: Button, manager: DialogManager):
    tree = manager.dialog_data["tree"]
    root = manager.dialog_data["root"]
    if manager.dialog_data.get("image_id") is None:
        image_id = tree.save_image_tree(root, "encoder")
    else:
        image_id = manager.dialog_data["image_id"]
    manager.dialog_data["image_id"] = image_id


async def delete_image(callback: CallbackQuery, button: Button, manager: DialogManager):
    if manager.dialog_data.get("image_id") is None:
        return
    image_id = manager.dialog_data["image_id"]
    os.remove(f'/home/danil/PycharmProjects/KUBSU_ndividual/graph theory/individual 2/tree_encoder_image_{image_id}.png')
    manager.dialog_data.pop("image_id")


async def go_to_main(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    await manager.start(MainState.main)











