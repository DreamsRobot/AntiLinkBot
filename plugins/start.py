from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello!\n\n"
        "I am **AntiLink Bot** 🚫\n\n"
        "Add me to your group and use:\n"
        "`/antilink enable` → Block links in bios/messages\n"
        "`/antilink disable` → Turn off AntiLink\n\n"
        "Admins only can control me."
    )
