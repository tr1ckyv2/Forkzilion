"""
Telegram Channel Media Downloader Plugin for userbot.
usage: .geta channel_username [will  get all media from channel, tho there is limit of 3000 there to prevent API limits.]
       .getc number_of_messsages channel_username
By: @Zero_cool7870
"""
import os
import subprocess
from userbot.events import register
from userbot import TEMP_DOWNLOAD_DIRECTORY


location = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "temp")

@register(pattern=r"\.geta(?: |$)(.*)", outgoing=True)
async def get_media(event):
    tempdir = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "temp")
    try:
        os.makedirs(tempdir)
    except BaseException:
        pass
    channel_username = event.pattern_match.group(1)
    event = await event.edit("Downloading All Media From this Channel.")
    msgs = await event.client.get_messages(channel_username, limit=3000)
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    i = 0
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, tempdir)
            i += 1
            await event.edit(
                f"Downloading Media From this Channel.\n **DOWNLOADED : **`{i}`"
            )
    ps = subprocess.Popen(("ls", tempdir), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\\n'", "")
    await event.edit(f"Successfully downloaded {output} number of media files")


#CMD_HELP.update(
 #   {
#        "channel_download": f"""**Plugin : **`channel_download`
#**Telegram Channel Media Downloader Plugin for userbot.**
#  • **Syntax : **`.geta channel_username` 
#  • **Function : **__will  download all media from channel into your bot server but there is limit of 3000 to prevent API limits.__
#  
#  • **Syntax : **`.getc number channel_username` 
#  • **Function : **__will  download latest given number of media from channel into your bot server .__
#  
#**Note : **__The downloaded media files will be at__ `.ls {location}`"""
#    }
#)
