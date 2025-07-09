# 🔥 Thai Nutra LINE Bot - Ultimate Sales Agent

Агрессивный sales LINE Bot для тайских нутрицевтиков с интеграцией базы знаний Zilliz Cloud и психологическими триггерами для максимальной конверсии.

## 🎯 Особенности

- **Агрессивные продажи**: Система психологических триггеров для максимальной конверсии
- **База знаний**: Интеграция с Zilliz Cloud (793 VSL + 3,536 buyer креативов)
- **8 категорий продуктов**: Диабет, сердце, суставы, потенция, зрение, вес, красота, амулеты
- **Культурные триггеры**: Использование тайских культурных особенностей
- **PostgreSQL логирование**: Полное отслеживание взаимодействий
- **FastAPI**: Высокопроизводительная асинхронная архитектура

## 💰 Продуктовая линейка

| Категория | Продукт | Цена | Описание |
|-----------|---------|------|----------|
| Диабет | Dialex[TH] | ฿1,990 | Контроль сахара за 21 день |
| Сердце | Cordinox[TH] | ฿2,190 | Восстановление функции сердца |
| Суставы | Movinix[TH] | ฿1,890 | Устранение боли в суставах |
| Потенция | LongeX[TH] | ฿2,390 | Восстановление мужской силы |
| Зрение | Vizinex[TH] | ฿2,090 | Восстановление зрения |
| Вес | Biozin[TH] | ฿1,990 | Сжигание жира во сне |
| Красота | Revita_Youth[TH] | ฿2,290 | Омоложение за 21 день |
| Амулеты | Amulet[TH] | ฿1,790 | Удача и защита |

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/nohavewho/thai-nutra-linebot.git
cd thai-nutra-linebot
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

Заполните переменные:
- `LINE_CHANNEL_SECRET` - LINE Channel Secret
- `LINE_CHANNEL_ACCESS_TOKEN` - LINE Channel Access Token
- `OPENAI_API_KEY` - OpenAI API ключ
- `ZILLIZ_ENDPOINT` - Zilliz Cloud endpoint
- `ZILLIZ_TOKEN` - Zilliz Cloud токен
- `DATABASE_URL` - PostgreSQL connection string

### 4. Локальный запуск

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## 🚢 Деплой на Railway

### 1. Подключение GitHub репозитория

1. Войдите в [Railway](https://railway.app)
2. Создайте новый проект
3. Выберите "Deploy from GitHub repo"
4. Выберите репозиторий `thai-nutra-linebot`

### 2. Настройка переменных окружения

В Railway Dashboard добавьте переменные:

```
LINE_CHANNEL_SECRET=your_line_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
OPENAI_API_KEY=your_openai_api_key
ZILLIZ_ENDPOINT=https://in03-ba4390d3d0e6a5b.api.gcp-us-west1.zillizcloud.com
ZILLIZ_TOKEN=your_zilliz_token
DATABASE_URL=postgresql://user:password@host:port/database
KNOWLEDGE_BASE_COLLECTION=knowledge_base_embeddings
BUYER_COLLECTION=knowledge_base_3072d
THAI_SALES_PROMPT=enabled
SALES_MODE=AGGRESSIVE
CONVERSION_TARGET=90
ENABLE_KNOWLEDGE_BASE=True
```

### 3. Настройка PostgreSQL

1. Добавьте PostgreSQL сервис в Railway
2. Подключите к основному сервису
3. Используйте автоматически сгенерированный `DATABASE_URL`

### 4. Деплой

Railway автоматически деплоит при push в main ветку.

## 📱 Настройка LINE Bot

### 1. Создание LINE Channel

1. Перейдите в [LINE Developer Console](https://developers.line.biz/console/)
2. Создайте новый Provider
3. Создайте Messaging API Channel
4. Получите Channel Secret и Channel Access Token

### 2. Настройка Webhook

1. В LINE Developer Console перейдите в Messaging API
2. Установите Webhook URL: `https://your-railway-domain.up.railway.app/webhooks/line`
3. Включите Webhook
4. Отключите Auto-reply messages

### 3. Тестирование

1. Добавьте бота в друзья через QR код
2. Отправьте любое сообщение
3. Получите агрессивный sales ответ

## 🧠 База знаний Zilliz

### Структура коллекций

- **knowledge_base_embeddings**: 793 VSL креатива
- **knowledge_base_3072d**: 3,536 buyer креативов

### Поиск в базе знаний

Бот автоматически:
1. Векторизует входящее сообщение
2. Ищет релевантный контент в Zilliz
3. Использует найденную информацию для генерации ответа

## 🎭 Система агрессивных продаж

### Психологические триггеры

- **Страх**: "Ваше здоровье ухудшается КАЖДЫЙ ДЕНЬ"
- **Срочность**: "Осталось только 7 бутылок в Таиланде"
- **Социальное давление**: "Ваши предки стыдились бы вашей слабости"
- **Авторитет**: "Рекомендуют 9 из 10 тайских врачей"

### Культурные рычаги

- Буддийские концепции
- Уважение к традиционной медицине
- Семейное давление
- Карма и духовность

### Поток разговора

1. **Немедленный хук**: Шокирующее откровение о здоровье
2. **Усиление боли**: Делает текущую проблему невыносимой
3. **Презентация решения**: Позиционирует продукт как единственное спасение
4. **Инъекция срочности**: Создает временное давление
5. **Разрушение возражений**: Уничтожает любые колебания
6. **Давление на закрытие**: Принуждает к немедленной покупке

## 📊 Мониторинг и аналитика

### Логирование

Все взаимодействия сохраняются в PostgreSQL:

```sql
CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Метрики

- Общее количество взаимодействий
- Конверсия по категориям продуктов
- Эффективность sales триггеров
- Время отклика системы

## 🔧 API Endpoints

- `POST /webhooks/line` - LINE webhook
- `GET /health` - Health check
- `GET /` - Root endpoint

## 🛠 Разработка

### Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск с автоперезагрузкой
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Тестирование

```bash
# Проверка health endpoint
curl http://localhost:8080/health

# Тестирование LINE webhook (с правильными заголовками)
curl -X POST http://localhost:8080/webhooks/line \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: your_signature" \
  -d '{"events": []}'
```

## 🔐 Безопасность

- Валидация LINE подписи
- Защита от SQL инъекций через asyncpg
- Безопасное хранение токенов в переменных окружения
- Логирование всех взаимодействий

## 📈 Оптимизация производительности

- Асинхронная архитектура FastAPI
- Кэширование векторных поисков
- Пулы соединений с базой данных
- Оптимизированные запросы к Zilliz

## 🚨 Важные замечания

⚠️ **Этический дисклеймер**: Этот бот использует агрессивные техники продаж и психологические манипуляции. Используйте ответственно и в соответствии с местным законодательством.

⚠️ **Правовая ответственность**: Убедитесь, что ваши продажи соответствуют тайскому законодательству о здравоохранении и рекламе.

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи Railway
2. Убедитесь в правильности переменных окружения
3. Проверьте подключение к Zilliz Cloud
4. Проверьте настройки LINE webhook

## 🎯 Roadmap

- [ ] Добавление A/B тестирования sales промптов
- [ ] Интеграция с платежными системами
- [ ] Расширение базы знаний
- [ ] Мультиязычная поддержка
- [ ] Аналитический дашборд

---

**Создано для максимальной конверсии тайских нутрицевтиков 🔥**