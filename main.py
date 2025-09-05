from pyrogram import Client
import config

plugins = dict(root="plugins")

app = Client(
    "AntiLinkBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=plugins
)

print("🤖 AntiLink Bot is running...")
app.run()
