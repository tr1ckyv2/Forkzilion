import io
import os
import random
from telethon.tl.types import InputMessagesFilterDocument

from userbot.events import register
from userbot import CMD_HELP 

@register(pattern=r"^\.cat$", outgoing=True)
async def cats(event):
    await event.edit("`Processing...`")
    CAT_GIF = await get_cat_gif(event.client, "@meowkingdom")
    await event.client.send_file(
        event.chat_id,
        reply_to=event.message.reply_to_msg_id,
        CAT_GIF,)
    # cleanup
    try:
        os.remove(CAT_GIF)
    except BaseException:
        pass

async def get_cat_gif(client, channel_id, search_kw=""):
    cat_gif_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
        search=search_kw,
    )
    cat_gif_message = random.choice(font_file_message_s)
    return await client.download_media(cat_gif_message)
