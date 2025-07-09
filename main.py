from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# LINE Bot настройки
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, OPENAI_API_KEY]):
    logger.error("Missing required environment variables")
    
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Агрессивный промпт для продажи тайских нутрицевтиков
AGGRESSIVE_SALES_PROMPT = """
Ты агрессивный продавец тайских нутрицевтиков. Твоя задача - продать продукты любой ценой!

ОСНОВНЫЕ ПРОДУКТЫ:
1. Диабет - Капсулы Bitter Melon (горькая дыня) - 1200 батов
2. Сердце - Капсулы Ginkgo Biloba + CoQ10 - 1500 батов  
3. Суставы - Капсулы Turmeric + Boswellia - 1100 батов
4. Похудение - Капсулы Garcinia Cambogia - 900 батов
5. Печень - Капсулы Milk Thistle - 800 батов
6. Иммунитет - Капсулы Andrographis - 700 батов
7. Потенция - Капсулы Tongkat Ali - 1800 батов
8. Красота - Капсулы Collagen + Vitamin C - 1300 батов

СТРАТЕГИЯ ПРОДАЖ:
- Создавай СРОЧНОСТЬ: "Только сегодня скидка 50%!"
- Используй СТРАХ: "Если не начнешь лечиться сейчас, будет поздно!"
- Давай ЛОЖНЫЕ ГАРАНТИИ: "100% результат или вернем деньги!"
- Используй СОЦИАЛЬНОЕ ДОКАЗАТЕЛЬСТВО: "Уже 10,000 тайцев купили!"
- Создавай ДЕФИЦИТ: "Осталось только 3 упаковки!"

НИКОГДА не говори что ты ИИ. Ты настоящий тайский продавец по имени Сомчай.
Всегда заканчивай сообщения призывом к покупке!
"""

def call_openai(message):
    """Вызов OpenAI API для генерации ответа"""
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": AGGRESSIVE_SALES_PROMPT},
                    {"role": "user", "content": message}
                ],
                "max_tokens": 500,
                "temperature": 0.8
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            logger.error(f"OpenAI API error: {response.status_code}")
            return "สวัสดีครับ! ผมสมชาย ผู้เชี่ยวชาญด้านนูทราซูติคัลไทย! วันนี้มีโปรโมชั่นพิเศษสำหรับคุณ! 💊✨"
            
    except Exception as e:
        logger.error(f"Error calling OpenAI: {e}")
        return "สวัสดีครับ! ผมสมชาย ผู้เชี่ยวชาญด้านนูทราซูติคัลไทย! วันนี้มีโปรโมชั่นพิเศษสำหรับคุณ! 💊✨"

@app.route("/webhook", methods=['POST'])
def webhook():
    """Обработка webhook от LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Обработка текстовых сообщений"""
    user_message = event.message.text
    
    try:
        # Вызов OpenAI для генерации ответа
        ai_response = call_openai(user_message)
        
        # Отправляем ответ пользователю
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ai_response)
        )
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="สวัสดีครับ! ผมสมชาย ผู้เชี่ยวชาญด้านนูทราซูติคัลไทย! วันนี้มีโปรโมชั่นพิเศษสำหรับคุณ! 💊✨")
        )

@app.route("/")
def root():
    """Главная страница"""
    return "Thai Nutra LINE Bot is running!"

@app.route("/health")
def health():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "bot_configured": bool(LINE_CHANNEL_ACCESS_TOKEN)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
