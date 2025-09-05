import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ANTILINK_STATUS, WARNINGS

LINK_PATTERN = re.compile(r"(https?://\S+|t\.me/\S+|@\w+)")

# --- Helper: Check Admin ---
async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

# --- Enable / Disable Command ---
@Client.on_message(filters.command("antilink") & filters.group)
async def toggle_antilink(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(client, chat_id, user_id):
        return await message.reply_text("❌ Only group admins can use this command.")

    if len(message.command) < 2:
        return await message.reply_text("Usage: `/antilink enable` or `/antilink disable`", quote=True)

    option = message.command[1].lower()
    if option == "enable":
        ANTILINK_STATUS[chat_id] = True
        await message.reply_text("✅ AntiLink has been **enabled** in this group.")
    elif option == "disable":
        ANTILINK_STATUS[chat_id] = False
        await message.reply_text("❌ AntiLink has been **disabled** in this group.")
    else:
        await message.reply_text("Usage: `/antilink enable` or `/antilink disable`", quote=True)

# --- Monitor Messages ---
@Client.on_message(filters.text & filters.group, group=1)
async def check_links(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    if not user or user.is_bot:
        return

    if not ANTILINK_STATUS.get(chat_id, False):
        return

    # Get user bio (about section)
    try:
        bio = (await client.get_chat(user.id)).bio or ""
    except:
        bio = ""

    text = message.text or ""
    if LINK_PATTERN.search(text) or LINK_PATTERN.search(bio):
        await message.delete()

        # Count warnings
        WARNINGS.setdefault(chat_id, {})
        WARNINGS[chat_id][user.id] = WARNINGS[chat_id].get(user.id, 0) + 1
        warn_count = WARNINGS[chat_id][user.id]

        if warn_count < 5:
            await message.reply_text(
                f"⚠️ {user.mention}, you have a link in your bio!\n"
                f"Warning {warn_count}/5. Remove it or you will be muted."
            )
        else:
            try:
                await client.restrict_chat_member(
                    chat_id,
                    user.id,
                    permissions={}
                )
                buttons = [
                    [InlineKeyboardButton("✅ Unmute User", callback_data=f"unmute_{user.id}")],
                    [InlineKeyboardButton("🗑 Clear Warns", callback_data=f"clear_{user.id}")]
                ]
                await message.reply_text(
                    f"🚫 {user.mention} has been muted for not removing links.",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            except Exception as e:
                await message.reply_text(f"❌ Failed to mute user: {e}")

# --- Handle Inline Buttons ---
@Client.on_callback_query(filters.regex("^(unmute|clear)_"))
async def handle_buttons(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = int(query.data.split("_")[1])

    if not await is_admin(client, chat_id, query.from_user.id):
        return await query.answer("❌ Only admins can use this.", show_alert=True)

    if query.data.startswith("unmute"):
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                permissions=query.message.chat.permissions  # restore permissions
            )
            await query.answer("✅ User unmuted.")
            await query.message.edit_text(f"🔊 User [{user_id}](tg://user?id={user_id}) has been unmuted.")
        except Exception as e:
            await query.answer(f"❌ Error: {e}", show_alert=True)

    elif query.data.startswith("clear"):
        if chat_id in WARNINGS and user_id in WARNINGS[chat_id]:
            WARNINGS[chat_id][user_id] = 0
        await query.answer("✅ Warnings cleared.")
        await query.message.edit_text(f"🗑 Warnings cleared for user [{user_id}](tg://user?id={user_id}).")
