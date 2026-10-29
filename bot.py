import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading

# ដាក់ Token របស់អ្នកនៅទីនេះ
TOKEN = '9147462762:AAGFKUv9rJ2xr949n7bw4IwwdC6hKwdMZNM'
bot = telebot.TeleBot(TOKEN)

user_lang = {}

def get_text(user_id, key):
    lang = user_lang.get(user_id, 'km')
    texts = {
        'km': {
            'welcome': "✨ **សូមស្វាគមន៍មកកាន់ PU PONG Store!** ✨\n\n📊 **ព័ត៌មានគណនីរបស់អ្នក**\n┣ 🆔 ID: `{user_id}`\n┗ 👤 ឈ្មោះ: {username}\n\n👇 សូមជ្រើសរើសម៉ឺនុយខាងក្រោម៖",
            'shop': "🛒 ហាងទំនិញ",
            'topup': "💰 បញ្ចូលប្រាក់",
            'history': "📦 ការបញ្ជាទិញ (History)",
            'lang': "🌐 ភាសា / Language",
            'choose_topup': "🇰🇭 **Bakong Pay - ជ្រើសរើសទឹកប្រាក់ (USD)**\n\nសូមជ្រើសរើសចំនួនទឹកប្រាក់ដែលអ្នកចង់បញ្ចូល៖",
        },
        'en': {
            'welcome': "✨ **Welcome to PU PONG Store!** ✨\n\n📊 **Account Info**\n┣ 🆔 ID: `{user_id}`\n┗ 👤 Name: {username}\n\n👇 Please select a menu below:",
            'shop': "🛒 Shop",
            'topup': "💰 Top Up",
            'history': "📦 Order History",
            'lang': "🌐 Language",
            'choose_topup': "🇰🇭 **Bakong Pay - Select Amount (USD)**\n\nPlease select the amount you want to top up:",
        }
    }
    return texts[lang].get(key, key)

# ១. ពេលចុច /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    username_str = f"@{username}" if username else f"ID: {user_id}"

    text = get_text(user_id, 'welcome').format(user_id=user_id, username=username_str)
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(get_text(user_id, 'shop'), callback_data='shop_menu'),
        InlineKeyboardButton(get_text(user_id, 'topup'), callback_data='topup_menu'),
        InlineKeyboardButton(get_text(user_id, 'history'), callback_data='order_history'),
        InlineKeyboardButton(get_text(user_id, 'lang'), callback_data='change_lang')
    )

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# ២. ប្រព័ន្ធគ្រប់គ្រងប៊ូតុងทั้งหมด
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id

    # ប្តូរភាសា
    if call.data == 'change_lang':
        current = user_lang.get(user_id, 'km')
        user_lang[user_id] = 'en' if current == 'km' else 'km'
        bot.answer_callback_query(call.id, "Changed Language / បានប្តូរភាសា")
        send_welcome_edit(call)

    # ម៉ឺនុយហាង (Shop)
    elif call.data == 'shop_menu':
        shop_text = (
            "📦 **សូមជ្រើសរើសប្រភេទផលិតផល៖**\n\n"
            "• **Robux Send** (ផ្ញើចូលក្នុង Game ផ្ទាល់)\n"
            "• **Robux Plus** (តាមប្រព័ន្ធ Gamepass/Pending)\n\n"
            "👇 សូមជ្រើសរើសប្រភេទខាងក្រោម៖"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💎 Robux Send", callback_data='r_send'))
        markup.add(InlineKeyboardButton("⭐ Roblox Plus", callback_data='r_plus'))
        markup.add(InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='back_home'))
        bot.edit_message_text(shop_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # ផលិតផល Roblox Plus
    elif call.data == 'r_plus':
        text = (
            "⭐ **Price List - Roblox Plus**\n\n"
            "• 400 Robux - $3.00\n"
            "• 800 Robux - $6.00\n"
            "• 1700 Robux - $12.00\n\n"
            "👇 សូមជ្រើសរើសកញ្ចប់ដែលអ្នកចង់ទិញ៖"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 ទិញ 400 Robux ($3.00)", callback_data='pay_amt_3.00'))
        markup.add(InlineKeyboardButton("🛒 ទិញ 800 Robux ($6.00)", callback_data='pay_amt_6.00'))
        markup.add(InlineKeyboardButton("🛒 ទិញ 1700 Robux ($12.00)", callback_data='pay_amt_12.00'))
        markup.add(InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='shop_menu'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # ផលិតផល Robux Send (បន្ថែមครบทุกราคาตามที่คุณต้องการ)
    elif call.data == 'r_send':
        text = (
            "💎 **Price List - Robux Send**\n\n"
            "• 100 Robux - $1.00\n"
            "• 200 Robux - $1.80\n"
            "• 400 Robux - $3.89\n"
            "• 500 Robux - $4.50\n"
            "• 1000 Robux - $8.50\n\n"
            "👇 សូមជ្រើសរើសកញ្ចប់ដែលអ្នកចង់ទិញ៖"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 ទិញ 100 Robux ($1.00)", callback_data='pay_amt_1.00'))
        markup.add(InlineKeyboardButton("🛒 ទិញ 200 Robux ($1.80)", callback_data='pay_amt_1.80'))
        markup.add(InlineKeyboardButton("🛒 ទិញ 400 Robux ($3.89)", callback_data='pay_amt_3.89'))
        markup.add(InlineKeyboardButton("🛒 ទិញ 500 Robux ($4.50)", callback_data='pay_amt_4.50'))
        markup.add(InlineKeyboardButton("🔥 ទិញ 1000 Robux ($8.50)", callback_data='pay_amt_8.50'))
        markup.add(InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='shop_menu'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # ម៉ឺនុយបញ្ចូលប្រាក់ (Top Up)
    elif call.data == 'topup_menu':
        text = get_text(user_id, 'choose_topup')
        markup = InlineKeyboardMarkup(row_width=3)
        markup.add(
            InlineKeyboardButton("$0.25", callback_data='pay_amt_0.25'),
            InlineKeyboardButton("$0.50", callback_data='pay_amt_0.50'),
            InlineKeyboardButton("$0.75", callback_data='pay_amt_0.75'),
            InlineKeyboardButton("$1.00", callback_data='pay_amt_1.00'),
            InlineKeyboardButton("$1.50", callback_data='pay_amt_1.50'),
            InlineKeyboardButton("$2.00", callback_data='pay_amt_2.00'),
            InlineKeyboardButton("$2.50", callback_data='pay_amt_2.50'),
            InlineKeyboardButton("$3.00", callback_data='pay_amt_3.00')
        )
        markup.add(InlineKeyboardButton("⬅️ Back", callback_data='back_home'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # ពេលជ្រើសរើសទឹកប្រាក់ ឬកញ្ចប់ទំនិញ -> បង្ហាញ QR Code និងកំណត់ពេល ២ នាទី (១២០ វិនាទី)
    elif call.data.startswith('pay_amt_'):
        amount = call.data.split('_')[2]
        username = call.from_user.username
        username_str = f"@{username}" if username else f"ID: {user_id}"

        qr_caption = (
            f"📸 **KHQR - Bakong Payment**\n\n"
            f"• **អតិថិជន:** {username_str}\n"
            f"• **ទឹកប្រាក់ត្រូវបង់:** ${amount}\n\n"
            f"⚠️ **បញ្ជាក់:** QR Code នេះមានសុពលភាពត្រឹម **២ នាទី** ប៉ុណ្ណោះ!"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ ខ្ញុំបានបង់ប្រាក់រួចរាល់", callback_data=f"paid_topup_{amount}"))
        markup.add(InlineKeyboardButton("⬅️ Back", callback_data='shop_menu'))

        bot.delete_message(call.message.chat.id, call.message.message_id)
        try:
            with open('qrcode.jpg', 'rb') as photo:
                sent_msg = bot.send_photo(call.message.chat.id, photo, caption=qr_caption, parse_mode="Markdown", reply_markup=markup)
            
            # កំណត់ពេល ២ នាទី (១២០ វិនាទី) មុននឹងលុប QR Code ចោលស្វ័យប្រវត្តិ
            def expire_qr(chat_id, msg_id):
                time.sleep(120)  # ១២០ វិនាទី = ២ នាទី
                try:
                    bot.delete_message(chat_id, msg_id)
                    bot.send_message(chat_id, "⌛ **QR Code បានផុតកំណត់ (Expired - ២ នាទី) ហើយត្រូវបានលុបចោល!**", parse_mode="Markdown")
                except:
                    pass
            threading.Thread(target=expire_qr, args=(sent_msg.chat.id, sent_msg.message_id)).start()
        except:
            bot.send_message(call.message.chat.id, "⚠️ រកមិនឃើញឯកសារ QR Code (`qrcode.jpg`) ទេ។")

    # ពេលចុចបញ្ជាក់ការបង់ប្រាក់រួច -> ចេញ Receipt និងប៊ូតុងឆាតទៅ Admin (@nhngheii)
    elif call.data.startswith('paid_topup_'):
        amt = call.data.split('_')[2]
        user = call.from_user
        username_str = f"@{user.username}" if user.username else f"ID: {user.id}"
        order_time = time.strftime('%Y-%m-%d %H:%M:%S')

        receipt = (
            f"🧾 **វិក្កយបត្របញ្ជាក់ការបង់ប្រាក់ (RECEIPT)**\n"
            f"----------------------------------------\n"
            f"• 👤 **អតិថិជន:** {username_str}\n"
            f"• 💰 **ទឹកប្រាក់:** ${amt}\n"
            f"• ⏰ **ម៉ោងកុម្ម៉ង់:** {order_time}\n"
            f"• 📌 **ស្ថានភាព:** ⏳ រង់ចាំ Admin ពិនិត្យផ្ទៀងផ្ទាត់\n"
            f"----------------------------------------\n"
            f"✨ សូមអរគុណសម្រាប់ការទិញទំនិញពីហាងយើងខ្ញុំ!"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💬 ឆាតទៅ Admin", url="https://t.me/nhngheii"))
        markup.add(InlineKeyboardButton("🏠 ត្រឡប់ទៅមឺនុយដើម", callback_data='back_home'))
        
        bot.answer_callback_query(call.id, "✅ បានផ្ញើវិក្កយបត្រជូន Admin!")
        try:
            bot.edit_message_caption(receipt, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, receipt, parse_mode="Markdown", reply_markup=markup)

        admin_alert = (
            f"🔔 **មានអតិថិជនបង់ប្រាក់ថ្មី!**\n\n"
            f"👤 **អតិថិជន:** {username_str}\n"
            f"💰 **តម្លៃ:** ${amt}\n"
            f"⏰ **ពេលវេលា:** {order_time}\n\n"
            f"👉 សូម Admin ឆែក App ធនាគារដើម្បីផ្ទៀងផ្ទាត់!"
        )
        bot.send_message(call.message.chat.id, admin_alert, parse_mode="Markdown")

    # ប្រវត្តិនៃការបញ្ជាទិញ (Order History)
    elif call.data == 'order_history':
        history_text = (
            "📦 **ប្រវត្តិនៃការបញ្ជាទិញ (Order History)**\n\n"
            "• គ្មានប្រវត្តិទិញទំនិញថ្មីៗទេឥឡូវនេះ។\n\n"
            "👇 សូមជ្រើសរើសម៉ឺនុយខាងក្រោម៖"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data='back_home'))
        bot.edit_message_text(history_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # ត្រឡប់ទៅមឺនុយដើម
    elif call.data == 'back_home':
        send_welcome_edit(call)

def send_welcome_edit(call):
    user_id = call.from_user.id
    username = call.from_user.username
    username_str = f"@{username}" if username else f"ID: {user_id}"

    text = get_text(user_id, 'welcome').format(user_id=user_id, username=username_str)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(get_text(user_id, 'shop'), callback_data='shop_menu'),
        InlineKeyboardButton(get_text(user_id, 'topup'), callback_data='topup_menu'),
        InlineKeyboardButton(get_text(user_id, 'history'), callback_data='order_history'),
        InlineKeyboardButton(get_text(user_id, 'lang'), callback_data='change_lang')
    )
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# ចាប់ផ្តើមដំណើរការ Bot
print("Bot Pro is running...")
bot.infinity_polling()