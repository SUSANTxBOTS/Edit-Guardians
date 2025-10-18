import os
import logging
from pymongo import MongoClient
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.helpers import mention_html
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
MONGO_URL = os.getenv("MONGO_URL")
CHANNEL_URL = os.getenv("CHANNEL_URL")
SUPPORT_GROUP_URL = os.getenv("SUPPORT_GROUP_URL")

mongo_client = MongoClient(MONGO_URL)
db = mongo_client["NYCREATION"]
users_col = db["users"]
groups_col = db["groups"]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        users_col.update_one({"_id": user.id}, {"$set": {"name": user.full_name}}, upsert=True)
    elif chat.type in ["group", "supergroup"]:
        groups_col.update_one({"_id": chat.id}, {"$set": {"title": chat.title}}, upsert=True)

    keyboard = [
        [InlineKeyboardButton("📢𝑺𝒖𝒑𝒑𝒐𝒓𝒕", url=CHANNEL_URL)],
        [InlineKeyboardButton("💬 𝑺𝒖𝒑𝒑𝒐𝒓𝒕 𝑮𝒓𝒐𝒖𝒑", url=SUPPORT_GROUP_URL)],
        [InlineKeyboardButton("ℹ️ 𝑯𝒆𝒍𝒑", callback_data="help")]
    ]

     image_url = "https://files.catbox.moe/vqomxt.jpg"
        mention = f'<a href="tg://openmessage?user_id={user.id}">{user.first_name}</a>'
    text = (
        "✨ <b>𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 𝑬𝒅𝒊𝒕 𝑮𝒖𝒂𝒓𝒅𝒊𝒂𝒏 𝑩𝒐𝒕</b> ✨\n\n"
        "🔹 𝑻𝒉𝒊𝒔 𝒃𝒐𝒕 𝒂𝒖𝒕𝒐𝒎𝒂𝒕𝒊𝒄𝒂𝒍𝒍𝒚 <b>𝒅𝒆𝒍𝒆𝒕𝒆𝒔 𝒆𝒅𝒊𝒕𝒆𝒅 𝒎𝒆𝒔𝒔𝒂𝒈𝒆𝒔</b> 𝒊𝒏 𝒈𝒓𝒐𝒖𝒑𝒔\n"
        "🔹 𝑯𝒆𝒍𝒑𝒔 𝒎𝒂𝒊𝒏𝒕𝒂𝒊𝒏 𝒕𝒓𝒂𝒏𝒔𝒑𝒂𝒓𝒆𝒏𝒄𝒚 𝒊𝒏 𝒄𝒐𝒏𝒗𝒆𝒓𝒔𝒂𝒕𝒊𝒐𝒏𝒔.\n\n"
        "✅ 𝑨𝒅𝒅 𝒎𝒆 𝒊𝒏 𝒚𝒐𝒖𝒓 𝒈𝒓𝒐𝒖𝒑 & 𝒈𝒊𝒗𝒆 <b>𝑫𝒆𝒍𝒆𝒕𝒆 𝑴𝒆𝒔𝒔𝒂𝒈𝒆𝒔</b> 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏."
    )

    await update.message.reply_html(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        text = (
            "⚙️ <b><i>𝑯𝒆𝒍𝒑 𝑴𝒆𝒏𝒖</i></b>\n\n"
            "🔹 <b>Message Guardian:</b> If someone edits a message in group, bot will delete it.\n"
            "🔹 <b>Broadcast:</b> Only Admin can broadcast messages to all users & groups.\n\n"
            "✅ Make sure bot has <b>Delete Message</b> rights in groups."
        )
        await query.edit_message_text(text, parse_mode="HTML")


async def edited_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.edited_message
    if not message:
        return

    chat = message.chat
    user = message.from_user

    try:
        await message.delete()
        warn_text = f"⚠️ {mention_html(user.id, user.first_name)}, you edited a message so it was deleted."
        await chat.send_message(warn_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Failed to delete edited message: {e}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CURRENT_ADMIN_ID = 7574330905
    user_id = update.effective_user.id
    if user_id != ADMIN_ID and user_id != CURRENT_ADMIN_ID:
        return await update.message.reply_text("❌ You are not authorized to use this command.")

    if not context.args:
        return await update.message.reply_text("Usage: /broadcast <message>")

    text = " ".join(context.args)

    for user in users_col.find():
        try:
            await context.bot.send_message(chat_id=user["_id"], text=text)
        except Exception as e:
            logger.warning(f"Failed to send to user {user['_id']}: {e}")

    for group in groups_col.find():
        try:
            await context.bot.send_message(chat_id=group["_id"], text=text)
        except Exception as e:
            logger.warning(f"Failed to send to group {group['_id']}: {e}")

    await update.message.reply_text("✅ 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙨𝙚𝙣𝙩 𝙩𝙤 𝙖𝙡𝙡 𝙪𝙨𝙚𝙧𝙨 𝙖𝙣𝙙 𝙜𝙧𝙤𝙪𝙥𝙨.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(help_menu, pattern="help"))
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, edited_message_handler))
    application.add_handler(CommandHandler("broadcast", broadcast))

    logger.info("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()
