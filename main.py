from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import asyncpg
import httpx
from pydantic import BaseModel
import asyncio
from typing import Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Thai Nutra LINE Bot")

# LINE Bot настройки
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not all([LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, OPENAI_API_KEY]):
    raise ValueError("Missing required environment variables")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Простая база данных в памяти для тестирования
user_sessions = {}

class UserSession:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.conversation_history = []
        self.current_product_interest = None

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

async def call_openai(message: str, user_session: UserSession) -> str:
    """Вызов OpenAI API для генерации ответа"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
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
                return "Извините, произошла ошибка. Попробуйте позже."
                
    except Exception as e:
        logger.error(f"Error calling OpenAI: {e}")
        return "Извините, произошла ошибка. Попробуйте позже."

@app.post("/webhook")
async def webhook(request: Request):
    """Обработка webhook от LINE"""
    signature = request.headers.get('X-Line-Signature', '')
    body = await request.body()
    
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    return {"status": "ok"}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Обработка текстовых сообщений"""
    user_id = event.source.user_id
    user_message = event.message.text
    
    # Получаем или создаем сессию пользователя
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession(user_id)
    
    user_session = user_sessions[user_id]
    
    # Асинхронный вызов OpenAI
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        ai_response = loop.run_until_complete(call_openai(user_message, user_session))
        
        # Отправляем ответ пользователю
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ai_response)
        )
        
        # Сохраняем в историю
        user_session.conversation_history.append({
            "user": user_message,
            "bot": ai_response
        })
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Извините, произошла ошибка. Попробуйте позже.")
        )
    finally:
        loop.close()

@app.get("/")
async def root():
    """Главная страница"""
    return {"message": "Thai Nutra LINE Bot is running!"}

@app.get("/health")
async def health():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "bot_configured": bool(LINE_CHANNEL_ACCESS_TOKEN)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
