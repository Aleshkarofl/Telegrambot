import os
import certifi
import ssl
import telegram.request

ssl_context = ssl.create_default_context(cafile=certifi.where())
telegram.request._httpxrequest.DEFAULT_SSL_CONTEXT = ssl_context

from dotenv import load_dotenv  # Загружаем dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, filters, MessageHandler, CallbackContext
from telegram.request import HTTPXRequest  # Импортируем HTTPXRequest

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из .env

if not TOKEN:
    raise ValueError("❌ Ошибка: Переменная окружения BOT_TOKEN не найдена!")

# Устанавливаем параметры SSL (если это требуется)
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Создаем объект запроса (если нужен кастомный запрос)
request = HTTPXRequest()

# Создаем объект приложения (Оставляем ТОЛЬКО ОДИН!)
app = Application.builder().token(TOKEN).request(request).build()

# Список разрешенных пользователей
ALLOWED_USERS = {7293170941, 875693247, 415437436, 5626401090}  # Замени на реальные Telegram ID



ALLOWED_USERS = {7293170941, 875693247,415437436,5626401909}  # Замініть на реальні Telegram ID

TECH_CARDS = {
    "Кебаб м": "📌 Ингредиенты:\n-Лаваш 80г\n- Салат 35г\n- Томати – 30г\n- цибуля - 3г\n- Мясо – 90г\n- Соус – 70г",
    "🍕 Піца Маргарита": "📌 Інгредієнти:\n- Тісто – 200г\n- Томатний соус – 50г\n- Моцарела – 100г\n- Базилік – 10г",
    "🍜 Рамен": "📌 Інгредієнти:\n- Локшина – 150г\n- Бульйон – 300мл\n- Яйце – 1 шт\n- Свинина – 80г\n- Зелена цибуля – 10г"
}

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🚀 Почати", callback_data="start_button")],
        [InlineKeyboardButton("ℹ️ Допомога", callback_data="help_button")],
        [InlineKeyboardButton("📊 Статистика", callback_data="stats_button")],
        [InlineKeyboardButton("⚙️ Налаштування", callback_data="settings_button")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text("Готовий допомогти! Оберіть дію:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Готовий допомогти! Оберіть дію:", reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "start_button":
        await query.message.edit_text("✅ Ви натиснули 'Почати'. Чим можу допомогти?")

    elif query.data == "help_button":
        keyboard = [
            [InlineKeyboardButton("📄 Тех. карти", callback_data="tech_cards")],
            [InlineKeyboardButton("💳 Касові рішення", callback_data="cash_solutions")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Оберіть розділ:", reply_markup=reply_markup)

    elif query.data == "tech_cards":
        keyboard = [[InlineKeyboardButton(name, callback_data=f"recipe_{name}")] for name in TECH_CARDS.keys()]
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="help_button")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Оберіть страву:", reply_markup=reply_markup)

    elif query.data.startswith("recipe_"):
        dish_name = query.data.replace("recipe_", "")
        if dish_name in TECH_CARDS:
            keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="tech_cards")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(TECH_CARDS[dish_name], reply_markup=reply_markup)
        else:
            await query.message.edit_text("❌ Інформацію про страву не знайдено.")

    elif query.data == "cash_solutions":
        await query.message.edit_text("💳 Тут буде інформація про касові рішення.")

    elif query.data == "stats_button":
        await query.message.edit_text("📊 Тут буде статистика.")

    elif query.data == "settings_button":
        await query.message.edit_text("⚙️ Налаштування бота.")

    elif query.data == "back_to_main":
        await start(update, context)

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Ви написали: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Бот запущений...")
    import ssl
import telegram.request

telegram.request._httpxrequest.DEFAULT_SSL_CONTEXT = ssl._create_unverified_context()
app.run_polling()

if __name__ == '__main__':
    main()
