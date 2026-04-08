import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import sqlite3
import requests
import json
import re

# Bot settings
BOT_TOKEN = "8697100491:AAHFj14hZFIneFm2nWRNkpOrX6vshZsFu4o"

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_text = """
**Welcome to Advanced Search Bot 💬**

---

## What can I do?  
Search for any phone number, email, or even national ID inside large databases.

---

### Phone or Email Search:  
- Send the phone number directly like: 01011796996  
- Or send the email to search in leaks.

---

### National ID Analysis:  
- Use: /nid NationalID  
- Example: /nid 28007172400077

---

### Email Tools:  
- /ghunt example@gmail.com – Analyze Google account (photo, sites, comments)  
- /breachchecker example@email.com – Check leaks online

---

### Facebook Tools:  
- Get profile picture of a locked account - /fbp  
- Search inside posts - /fbsearch 01007185641

---

### Truecaller:  
- Advanced phone number search - /truecaller  
- Direct search - /truecaller 01006963330
    """

    keyboard = [
        [InlineKeyboardButton("🔍 Search by Phone", callback_data="search_phone")],
        [InlineKeyboardButton("📧 Search by Email", callback_data="search_email")],
        [InlineKeyboardButton("🆔 Analyze National ID", callback_data="nid_search")],
        [InlineKeyboardButton("📱 Truecaller", callback_data="truecaller")],
        [InlineKeyboardButton("🔐 Breach Check", callback_data="breach_check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_phone_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text.strip()

    if not re.match(r'^01[0-9]{9}$', phone_number):
        await update.message.reply_text("❌ Invalid phone number. Please enter a valid Egyptian phone number (11 digits)")
        return

    # Simulate database search
    await update.message.reply_text(f"🔍 Searching for number: {phone_number}")

    # Simulated results
    results = f"""
**Search results for number: {phone_number}**

📞 **Number Information:**
- Carrier: {get_carrier(phone_number)}
- Region: {get_region(phone_number)}

👤 **Personal Information:**
- Name: Mohamed Ahmed
- Governorate: Cairo

📱 **Truecaller:**
- Name: Mohamed Ahmed
- Photo: Available

🔐 **Breaches:**
- Number found in 3 breaches
- Last breach: 2023
    """

    await update.message.reply_text(results, parse_mode='Markdown')


async def nid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter the national ID after the command\nExample: /nid 28007172400077")
        return

    nid = context.args[0]

    if not re.match(r'^[0-9]{14}$', nid):
        await update.message.reply_text("❌ National ID must be 14 digits")
        return

    await update.message.reply_text(f"🔍 Analyzing national ID: {nid}")

    analysis = f"""
**National ID Analysis: {nid}**

📅 **Details:**
- Birth Date: {nid[5:7]}/{nid[3:5]}/19{nid[1:3]}
- Governorate: {get_governorate(nid[7:9])}
- Gender: {'Male' if int(nid[12]) % 2 == 1 else 'Female'}

📍 **Information:**
- Issuing Office: Cairo
- Serial Number: {nid[9:13]}
    """

    await update.message.reply_text(analysis, parse_mode='Markdown')


async def ghunt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter the email after the command\nExample: /ghunt example@gmail.com")
        return

    email = context.args[0]

    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await update.message.reply_text("❌ Invalid email address")
        return

    await update.message.reply_text(f"🔍 Analyzing Google account: {email}")

    analysis = f"""
**GHunt Analysis for: {email}**

👤 **Account Information:**
- Name: Mohamed Ahmed
- Photo: ✓ Available
- Account: ✓ Active

🌐 **Activities:**
- YouTube: ✓ Available
- Google Maps: ✓ Available
- Comments: 15 comments

📊 **Statistics:**
- Account created: 2020
- Last activity: 2024
    """

    await update.message.reply_text(analysis, parse_mode='Markdown')


async def breach_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter the email after the command\nExample: /breachchecker example@email.com")
        return

    email = context.args[0]

    await update.message.reply_text(f"🔍 Checking breaches for email: {email}")

    breach_info = f"""
**Breach Check for: {email}**

🔐 **Results:**
- Total breaches: 3
- Leaked passwords: 1
- Last breach: 2023

📋 **Detected Breaches:**
1. LinkedIn (2021)
2. Facebook (2022) 
3. Adobe (2023)

⚠️ **Recommendations:**
- Change your password
- Enable two-factor authentication
    """

    await update.message.reply_text(breach_info, parse_mode='Markdown')


async def truecaller_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter the phone number after the command\nExample: /truecaller 01006963330")
        return

    phone = context.args[0]

    await update.message.reply_text(f"🔍 Searching Truecaller for: {phone}")

    truecaller_info = f"""
**Truecaller Results for: {phone}**

👤 **Information:**
- Name: Mohamed Ahmed
- Email: mohamed.ahmed@gmail.com
- Governorate: Cairo

📞 **Number Details:**
- Carrier: Vodafone
- Type: Mobile
- Status: ✓ Active

📊 **Rating:**
- Score: 4.2/5
- Reviews count: 15
    """

    await update.message.reply_text(truecaller_info, parse_mode='Markdown')


async def facebook_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please enter phone number or ID after the command\nExample: /fbsearch 01007185641")
        return

    search_query = context.args[0]

    await update.message.reply_text(f"🔍 Searching Facebook for: {search_query}")

    fb_info = f"""
**Facebook Search Results for: {search_query}**

👤 **Profile:**
- Name: Mohamed Ahmed
- Photo: ✓ Available
- Friends: 350
- Posts: 45

📍 **Information:**
- Governorate: Cairo
- Job: Software Engineer
- Education: Cairo University

🔍 **Recent Posts:**
- 3 posts this month
- Last activity: Today
    """

    await update.message.reply_text(fb_info, parse_mode='Markdown')


# Helper functions
def get_carrier(phone):
    prefixes = {
        '010': 'Vodafone',
        '011': 'Etisalat', 
        '012': 'Orange',
        '015': 'WE'
    }
    return prefixes.get(phone[:3], 'Unknown')


def get_region(phone):
    regions = ['Cairo', 'Alexandria', 'Giza', 'Dakahlia', 'Sharqia']
    return regions[hash(phone) % len(regions)]


def get_governorate(code):
    gov_codes = {
        '01': 'Cairo', '02': 'Alexandria', '03': 'Port Said',
        '04': 'Suez', '11': 'Damietta', '12': 'Dakahlia',
        '13': 'Sharqia', '14': 'Qalyubia', '15': 'Kafr El-Sheikh',
        '16': 'Gharbia', '17': 'Monufia', '18': 'Beheira',
        '19': 'Ismailia', '21': 'Giza', '22': 'Beni Suef',
        '23': 'Fayoum', '24': 'Minya', '25': 'Assiut',
        '26': 'Sohag', '27': 'Qena', '28': 'Aswan',
        '29': 'Luxor', '31': 'Red Sea', '32': 'New Valley',
        '33': 'Matrouh', '34': 'North Sinai', '35': 'South Sinai'
    }
    return gov_codes.get(code, 'Unknown')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "search_phone":
        await query.edit_message_text("📞 Send phone number to search (Example: 01012345678)")
    elif query.data == "search_email":
        await query.edit_message_text("📧 Send email to search")
    elif query.data == "nid_search":
        await query.edit_message_text("🆔 Use command: /nid then the national ID (14 digits)")
    elif query.data == "truecaller":
        await query.edit_message_text("📱 Use command: /truecaller then the phone number")
    elif query.data == "breach_check":
        await query.edit_message_text("🔐 Use command: /breachchecker then the email")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("nid", nid_command))
    application.add_handler(CommandHandler("ghunt", ghunt_command))
    application.add_handler(CommandHandler("breachchecker", breach_checker))
    application.add_handler(CommandHandler("truecaller", truecaller_search))
    application.add_handler(CommandHandler("fbsearch", facebook_search))
    application.add_handler(CommandHandler("fbp", facebook_search))

    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_search))

    print("Bot is now running...")
    application.run_polling()


if __name__ == '__main__':
    main()
