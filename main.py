import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === Bot Configuration ===
BOT_TOKEN = "8016733680:AAEVDVv1RgLpznYmCTNaLgXXYqDLrleQhWU"
CHANNEL_USERNAME = "@BetProNetwork"
ADMIN_USER_ID = 1227342059

# === Logging Setup ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Join VIP", callback_data="vip")],
        [InlineKeyboardButton("Get Free Tips", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"👋 Hello {user.first_name}! Welcome to BetPro Network.\n\nChoose an option below:", reply_markup=reply_markup)

# === Callback Handler ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "vip":
        await query.edit_message_text(
            "💎 VIP Access Plans:\n\n"
            "🔹 Basic VIP: ₦5,000/month\n"
            "🔹 Elite VIP: ₦10,000/month\n"
            "🔹 Daily Pass: ₦1,000/day\n\n"
            "To subscribe, message the admin: @BetProNetwork"
        )

# === Admin Broadcast ===
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast Your message here.")
        return

    message = "🔊 Broadcast from Admin:\n\n" + " ".join(context.args)
    count = 0

    with open("users.txt", "r") as file:
        for line in file:
            user_id = line.strip()
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
                count += 1
            except Exception:
                continue

    await update.message.reply_text(f"✅ Message sent to {count} users.")

# === User Tracking ===
async def save_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    try:
        with open("users.txt", "a+") as f:
            f.seek(0)
            if user_id not in f.read():
                f.write(f"{user_id}\n")
    except Exception as e:
        logger.error(f"Error saving user: {e}")

# === Main ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("restart", start))
    app.add_handler(CommandHandler("reboot", start))
    app.add_handler(CommandHandler("start", save_user))  # Logs user on /start

    print("✅ Bot is running...")
    app.run_polling()
