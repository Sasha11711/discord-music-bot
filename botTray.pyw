import asyncio
import pystray
import bot
from PIL import Image
from config.settings import TRAY_ICON, TRAY_TITLE, TRAY_EXIT

loop = asyncio.get_event_loop()

def on_exit(icon: pystray._base.Icon, item):
    loop.call_soon_threadsafe(asyncio.create_task, bot.close())
    icon.stop()
    
icon = pystray.Icon(
    "discord_music_bot",
    Image.open(TRAY_ICON),
    TRAY_TITLE,
    pystray.Menu(
        pystray.MenuItem(TRAY_EXIT, on_exit)
    )
)

if __name__ == "__main__":
    
    icon.run_detached()
    loop.run_until_complete(bot.start())
