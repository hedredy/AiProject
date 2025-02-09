import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Установим API ключи
TELEGRAM_API_KEY = '7905118281:AAF9b025rc4g6lFy6BxJxYIXYDbE_OlQD3g'  # Замените на ваш Telegram API ключ
DEEPSEEK_API_KEY = 'sk-6d2c5b8cc905419ea28cee171b7d18b1'  # Замените на ваш DeepSeek API ключ

# Устанавливаем OpenAI API
openai.api_key = DEEPSEEK_API_KEY
openai.api_base = "https://api.deepseek.com"

# Функция для обработки сообщений
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне сообщение, и я использую DeepSeek для ответа.')

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Получаем текст сообщения от пользователя

    # Отправляем запрос в DeepSeek
    response = openai.ChatCompletion.create(
        model="deepseek-chat",  # Используем модель DeepSeek
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_message},
        ],
        stream=False  # Отправляем обычный ответ (не стрим)
    )

    # Получаем ответ и отправляем его пользователю
    bot_response = response.choices[0].message['content']
    update.message.reply_text(bot_response)

def main() -> None:
    # Создаем Updater и передаем ему ключ
    updater = Updater(TELEGRAM_API_KEY)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Регистрация обработчика для текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()

    # Ожидаем завершения
    updater.idle()

if __name__ == '__main__':
    main()
