import asyncio
import re
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from Haffman import HaffmanTree, Decoder, Encoder, RootTree
from main_dialog.states import MainState
import os


async def input_message_table(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    pattern = r"[\D|\t]{1} - \d+"
    text = message.text
    table = [tuple(i.split(" - ")) for i in re.findall(pattern, text)]
    if not table or len(table) < 2:
        await message.answer("Не корректные данные таблицы")
        return
    table_frequency = ("-----------------------\n" +
                       "".join([f"{str(i[0])} - {str(i[1])}\n " for i in table])
                       + "-----------------------\n")
    manager.dialog_data["table_decoder"] = table
    manager.dialog_data["table_frequency"] = table_frequency
    await manager.next()


async def input_message_code(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    pattern = r"[01]+"
    text = message.text
    code = re.findall(pattern, text)
    if len(code) == 1:
        table = sorted([RootTree(left=None, right=None, value=int(i[1]), info=f"{i[0]}")
                        for i in manager.dialog_data["table_decoder"]], key=lambda x: (x.value, x.info))
        tree_decoder = HaffmanTree("")
        decoder = Decoder(code[0])
        root_decoder = HaffmanTree.build_tree(analysis_list=table)
        encoder = Encoder("", dict())
        encoder.table_haffman(root_decoder, "")
        text_decoder = decoder.decode(root_decoder)
        manager.dialog_data["encoder_table_sim"] = encoder.view_table()
        manager.dialog_data["code_decoder"] = code[0]
        manager.dialog_data["text_decoder"] = text_decoder
        manager.dialog_data["tree_decoder"] = tree_decoder
        manager.dialog_data["root_decoder"] = root_decoder
        await manager.next()
        return
    await message.answer("Данные кода введены не верно, код состоит из 0 и 1")


async def get_tree_decoder_image(callback: CallbackQuery, button: Button, manager: DialogManager):
    tree = manager.dialog_data["tree_decoder"]
    root = manager.dialog_data["root_decoder"]
    if manager.dialog_data.get("image_decoder_id") is None:
        image_id = tree.save_image_tree(root, "decoder")
    else:
        image_id = manager.dialog_data["image_decoder_id"]
    manager.dialog_data["image_decoder_id"] = image_id


async def delete_image(callback: CallbackQuery, button: Button, manager: DialogManager):
    if manager.dialog_data.get("image_decoder_id") is None:
        return
    image_id = manager.dialog_data["image_decoder_id"]
    os.remove(f'/home/danil/PycharmProjects/KUBSU_ndividual/graph theory/individual 2/tree_decoder_image_{image_id}.png')
    manager.dialog_data.pop("image_decoder_id")


async def go_to_main(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    await manager.start(MainState.main)

