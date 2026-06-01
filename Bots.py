#!/usr/bin/env python3
"""
AKM Ads Market - Telegram Bot
Main entry point
"""

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import handlers and keyboards
from handlers import *
from keyboards import main_menu

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Register all message handlers
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_start, Command("menu"))
dp.message.register(help_command, Command("help"))
dp.message.register(cancel_handler, Command("cancel"))

# Register callback handlers
dp.callback_query.register(role_selected, lambda c: c.data.startswith("role_"))
dp.callback_query.register(process_channel_category, AddChannelState.waiting_for_category)
dp.callback_query.register(process_campaign_category, CreateCampaignState.waiting_for_category)

# Register message handlers for states
dp.message.register(process_add_funds, AddFundsState.waiting_for_amount)
dp.message.register(process_channel_id, AddChannelState.waiting_for_channel_id)
dp.message.register(process_channel_title, AddChannelState.waiting_for_title)
dp.message.register(process_channel_subs, AddChannelState.waiting_for_subscribers)
dp.message.register(process_channel_price, AddChannelState.waiting_for_price)
dp.message.register(process_campaign_title, CreateCampaignState.waiting_for_title)
dp.message.register(process_campaign_desc, CreateCampaignState.waiting_for_description)
dp.message.register(process_campaign_budget, CreateCampaignState.waiting_for_budget)
dp.message.register(process_campaign_price, CreateCampaignState.waiting_for_price_per_post)
dp.message.register(process_campaign_min_subs, CreateCampaignState.waiting_for_min_subs)

# Register regular message handlers
dp.message.register(show_dashboard, lambda m: m.text == "📊 Dashboard")
dp.message.register(show_wallet, lambda m: m.text == "💰 Wallet")
dp.message.register(add_funds_start, lambda m: m.text == "💳 Add Funds")
dp.message.register(add_channel_start, lambda m: m.text == "➕ Add Channel")
dp.message.register(create_campaign_start, lambda m: m.text == "✨ Create Campaign")
dp.message.register(browse_marketplace, lambda m: m.text == "🔍 Browse Marketplace")
dp.message.register(my_channels, lambda m: m.text == "📢 My Channels")
dp.message.register(my_campaigns, lambda m: m.text == "📈 My Campaigns")
dp.message.register(help_command, lambda m: m.text == "❓ Help")

async def main():
    """Main function to start bot"""
    logger.info("🤖 AKM Ads Market Bot Starting...")
    
    # Delete webhook (using polling)
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info(f"✅ Bot started! Username: {(await bot.get_me()).username}")
    logger.info("🚀 Bot is polling for updates...")
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")