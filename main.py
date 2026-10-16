from pyrogram import Client, filters
import requests
from deep_translator import GoogleTranslator

# ඔයාගේ Credentials
API_ID = 38657064
API_HASH = "453750680fe5eedab586db750c579c72"
BOT_TOKEN = "8621084667:AAGrNfeOwpl1H-6PYho3o6r2vICv2Mg4dLM"

app = Client(
    "BypassBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
def start_handler(client, message):
    welcome_text = (
        "👋 Hello! I am your Multi-Language Link Bypasser Bot.\n"
        "Send me any short link, and I will get the original link for you!\n\n"
        "👋 ආයුබෝවන්! මම ඕනෑම භාෂාවකින් වැඩ කරන Link Bypasser Bot කෙනෙක්.\n"
        "ඔයාගේ Short Link එක මට එවන්න!"
    )
    message.reply_text(welcome_text)

@app.on_message(filters.text & ~filters.command(["start"]))
def bypass_handler(client, message):
    text = message.text
    if "http" in text:
        try:
            detected_lang = GoogleTranslator(source='auto', target='en').detect(text)
        except:
            detected_lang = 'en'

        sent_msg = message.reply_text("⏳ Bypassing link... Please wait / පොඩ්ඩක් ඉන්න...")
        try:
            api_url = f"https://api.bypass.vip/bypass?url={text}"
            res = requests.get(api_url).json()
            
            if res.get("status") == "success":
                dest = res.get("destination")
                reply_text = f"✅ **Original Link:**\n`{dest}`"
                sent_msg.edit_text(reply_text)
            else:
                error_msg = "❌ Failed to bypass this link."
                if detected_lang == 'si':
                    error_msg = "❌ මේ Link එක Bypass කරන්න බැරි වුණා."
                sent_msg.edit_text(error_msg)
        except Exception as e:
            sent_msg.edit_text("❌ Error occurred! Try again later.")
    else:
        message.reply_text("⚠️ Please send a valid URL / කරුණාකර නිවැරදි Link එකක් එවන්න.")

print("🤖 Multi-Language Bot is running...")
app.run()
