import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = "8779758731:AAEhsNAFGycPMB6cY45jW5xaqFvfwCm8xWA"

# Simple welcome message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    
    # Create simple buttons
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/pythontelegramcommunity")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/pythontelegrambot")],
        [InlineKeyboardButton("✅ I've Joined", callback_data='joined')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        "Please join these channels to continue:",
        reply_markup=reply_markup
    )

async def joined_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when user clicks I've joined button."""
    query = update.callback_query
    await query.answer()
    
    # Simple message - no actual verification
    await query.edit_message_text(
        "✅ Thank you for joining!\n\n"
        "Here's your special content:\n"
        "• Secret Code: BOT12345\n"
        "• Special Link: https://t.me/pythontelegramcommunity\n\n"
        "Enjoy! 🎉"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    await update.message.reply_text("Send /start to begin!")

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(joined_button, pattern='joined'))

    # Start the Bot
    print("🤖 Bot is starting... Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
