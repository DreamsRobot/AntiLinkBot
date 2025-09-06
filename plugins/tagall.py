from pyrogram import Client, filters
from pyrogram.types import Message
import random

# Some emojis to use instead of usernames
EMOJIS = ["😀", "😎", "😂", "🥳", "🔥", "💫", "💖", "🕊️", "🌸", "⭐", "⚡", "🎯", "🌍"]

@Client.on_message(filters.command(["all", "tagall"], prefixes=["/", "@"]) & filters.group)
async def tag_all(client: Client, message: Message):
    # Get the message text after the command
    if len(message.command) > 1:
        custom_text = message.text.split(" ", 1)[1]
    else:
        custom_text = "Attention everyone!"

    # Fetch all members in the chat
    members = []
    async for m in client.get_chat_members(message.chat.id):
        members.append(m.user.id)

    # Build the tag message with emojis instead of usernames
    tags = []
    for i, user_id in enumerate(members, start=1):
        emoji = random.choice(EMOJIS)
        tags.append(f"{emoji}")

    # Telegram messages have a limit (4096 chars), so split if too big
    chunk_size = 50  # number of emojis per message
    for i in range(0, len(tags), chunk_size):
        text = custom_text + "\n\n" + " ".join(tags[i:i+chunk_size])
        await message.reply_text(text)
