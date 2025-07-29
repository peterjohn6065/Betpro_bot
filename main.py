import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
import os

# === CONFIGURATION ===
BOT_TOKEN = "5774041866:AAGpJrrgHd7cYV3NS_OavhzgeTEOBgZDLyg"
ADMIN_ID = 1227342059
CHANNEL_USERNAME = "@BetProNetwork"

# === LOGGER SETUP ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# === START COMMAND ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔥 Join VIP", callback_data="join_vip")],
        [InlineKeyboardButton("📊 Today's Predictions", callback_data="get_predictions")],
    ]
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "This is the official BetPro Bot for VFL and Sports Signals.\n"
        "Use the buttons below to explore.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# === VIP COMMAND ===
async def vip(update: Update, context:
