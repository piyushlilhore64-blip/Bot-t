import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8725750503:AAEu6QCctOyUKxUyJa-Gqpw8-bzCA6frDfk')

# List of channels to join (replace with your channel usernames)
# Format: @channelusername
REQUIRED_CHANNELS = [
    '@your_channel_1',  # Replace with your first channel
    '@your_channel_2',  # Replace with your second channel
    '@your_channel_3',  # Replace with your third channel
]

# Message to show after joining all channels
SUCCESS_MESSAGE = """✅ **Congratulations! You've joined all required channels!**

Here's your special content:
- Secret link: https://example.com
- Promo code: SECRET123
- Join our group: @your_group

Thank you for your support! 🎉"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with channel join buttons when /start is issued."""
    user = update.effective_user
    
    # Create inline keyboard with channel join buttons
    keyboard = []
    for channel in REQUIRED_CHANNELS:
        # Remove @ from channel name for the link
        channel_name = channel.replace('@', '')
        button = InlineKeyboardButton(
            f"Join {channel}", 
            url=f"https://t.me/{channel_name}"
        )
        keyboard.append([button])
    
    # Add verification button
    keyboard.append([InlineKeyboardButton("✅ I've joined all channels", callback_data='verify')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        "To access the content, you must join the following channels first:\n\n"
        "After joining all channels, click the verification button below.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def verify_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verify if user has joined all channels."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Check if user has joined all channels
    all_joined = True
    not_joined_channels = []
    
    for channel in REQUIRED_CHANNELS:
        try:
            # Try to get chat member status
            channel_username = channel.replace('@', '')
            member = await context.bot.get_chat_member(chat_id=f"@{channel_username}", user_id=user_id)
            
            # Check if user is member, administrator, or creator
            if member.status not in ['member', 'administrator', 'creator']:
                all_joined = False
                not_joined_channels.append(channel)
        except Exception as e:
            # If bot can't check (might not be admin in channel), assume they need to join
            logger.warning(f"Could not check channel {channel}: {e}")
            all_joined = False
            not_joined_channels.append(channel)
    
    if all_joined:
        # User has joined all channels - show success message
        keyboard = [[InlineKeyboardButton("🔗 Get Content", url="https://t.me/your_group")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            SUCCESS_MESSAGE,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        # User hasn't joined all channels
        channel_list = "\n".join([f"• {ch}" for ch in not_joined_channels])
        
        # Create keyboard with missing channels
        keyboard = []
        for channel in not_joined_channels:
            channel_name = channel.replace('@', '')
            button = InlineKeyboardButton(
                f"Join {channel}", 
                url=f"https://t.me/{channel_name}"
            )
            keyboard.append([button])
        
        keyboard.append([InlineKeyboardButton("🔄 Check Again", callback_data='verify')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"❌ You haven't joined all required channels yet!\n\n"
            f"Missing channels:\n{channel_list}\n\n"
            "Please join them and click 'Check Again'.",
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /help is issued."""
    await update.message.reply_text(
        "Use /start to begin the verification process.\n"
        "Join all required channels to access the content."
    )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(verify_button, pattern='verify'))

    # Start the Bot
    print("🤖 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()