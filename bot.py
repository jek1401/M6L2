import telebot
from fusion_brain import FusionBrainAPI  # импорт класса из другого файла

# Замените на токен вашего Telegram-бота
TELEGRAM_TOKEN = '8160447654:AAFPhtJVVXdf9pTiwD3u6M6xcFcvObZCNbo'
API_KEY = '47C2E81B1EF6118EE129CF3F04C05DE5'
SECRET_KEY = '26FB5B2E21ADA950460BECEC36D6DA24'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Хэндлер для обработки всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    bot.send_message(message.chat.id, f"Сейчас сгенерирую картинку по запросу: '{prompt}'")

    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    image_path = f"{message.chat.id}_result.jpg"

    try:
        api.generate_image(prompt, save_path=image_path)
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.send_message(message.chat.id, f"\u041eшибка при генерации: {str(e)}")

if __name__ == '__main__':
    print("\u0411\u043e\u0442 \u0437\u0430\u043f\u0443\u0449\u0435\u043d!")
    bot.infinity_polling()