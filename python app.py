from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os
import re

# ضعي هنا الـ TOKEN اللي حصلتي عليه من BotFather
TOKEN = "8525718976:AAFqOAzW7Y899ljT5iRiNhBkV1ZSyPobkwg"

# مجلد التحميل
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# منع البلاي ليست
def is_playlist(url: str) -> bool:
    return "playlist" in url or "list=" in url

# رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ابعتي رابط *فيديو واحد فقط* من يوتيوب\n"
        "❌ البلاي ليست غير مدعومة",
        parse_mode="Markdown"
    )

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if is_playlist(url):
        await update.message.reply_text("❌ البوت يدعم فيديو واحد فقط، مش قائمة تشغيل")
        return

    await update.message.reply_text("⏳ جاري التحميل...")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'format': 'bestvideo[height<=720]+bestaudio/best',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename = re.sub(r'\.\w+$', '.mp4', filename)

        await update.message.reply_video(
            video=open(filename, "rb"),
            caption="✅ تم التحميل"
        )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ حصل خطأ:\n{e}")

# تشغيل البوت
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
