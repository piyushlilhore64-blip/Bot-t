import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = "8779758731:AAEhsNAFGycPMB6cY45jW5xaqFvfwCm8xWA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with buttons when /start is issued."""
    # Create buttons
    keyboard = [
        [InlineKeyboardButton("📚 About Us", callback_data='about')],
        [InlineKeyboardButton("🛍️ Our Products", callback_data='products')],
        [InlineKeyboardButton("📞 Contact", callback_data='contact')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Welcome! Choose an option below:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses and show information."""
    query = update.callback_query
    await query.answer()
    
    # Get the button that was pressed
    button_pressed = query.data
    
    # Show different info based on button pressed
    if button_pressed == 'about':
        message = "📚 **About Us**\n\nWe are a simple Telegram bot created to demonstrate buttons.\n\nStarted in 2024, we provide information at your fingertips!"
        
    elif button_pressed == 'products':
        message = "🛍️ **Our Products**\n\n• Product 1: Cool Gadget - $10\n• Product 2: Awesome Tool - $20\n• Product 3: Super Service - $30\n\nClick /start to return to menu."
        
    elif button_pressed == 'contact':
        message = "📞 **Contact Us**\n\n📧 Email: example@email.com\n📱 Telegram: @username\n🌐 Website: www.example.com"
        
    elif button_pressed == 'help':
        message = "❓ **Help**\n\nUse the buttons below to navigate.\n\n• About: Learn about us\n• Products: See our items\n• Contact: Get in touch\n\nSend /start anytime to return to menu."
    
    else:
        message = "Unknown option"
    
    # Create back button to return to main menu
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main menu."""
    query = update.callback_query
    await query.answer()
    
    # Show main menu again
    keyboard = [
        [InlineKeyboardButton("📚 About Us", callback_data='about')],
        [InlineKeyboardButton("🛍️ Our Products", callback_data='products')],
        [InlineKeyboardButton("📞 Contact", callback_data='contact')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "👋 Welcome back! Choose an option below:",
        reply_markup=reply_markup
    )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^(about|products|contact|help)$'))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='^back_to_menu$'))

    # Start the Bot
    print("🤖 Bot is starting... Press Ctrl+C to stop")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
