import os

# Telegram API details
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# Database in memory (reset on restart)
ANTILINK_STATUS = {}   # {chat_id: True/False}
WARNINGS = {}          # {chat_id: {user_id: warn_count}}
